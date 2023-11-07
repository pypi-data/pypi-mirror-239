import os
import asyncio
import aiosqlite
from aiosqlite import Cursor, Connection
import pandas as pd
from bioservices import BioDBNet
from multiprocessing import Value
from typing import Union, List, Iterable

from pandas import DataFrame

from async_bioservices.input_database import InputDatabase
from async_bioservices.output_database import OutputDatabase
from async_bioservices.taxon_id import TaxonID


class _db2db:
    biodbnet: BioDBNet = None
    
    def __init__(self, quiet: bool, async_cache: bool, bioservices_cache: bool):
        if _db2db.biodbnet is None:
            biodbnet = BioDBNet(verbose=not quiet, cache=bioservices_cache)  # Invert quiet to verbose
            biodbnet.services.settings.TIMEOUT = 60
            _db2db.biodbnet = biodbnet
        
        self.cache: bool = async_cache
        self._table_name: str = "db2db"
        self.biodbnet = _db2db.biodbnet
        self.connection: Connection = None
        self._db_columns: List[str] = ["id", "taxon_id"]
    
    @classmethod
    async def init(cls, quiet: bool, async_cache: bool, biodbnet_cache: bool) -> "_db2db":
        instance = cls(quiet=quiet, async_cache=async_cache, bioservices_cache=biodbnet_cache)
        
        database_dir = _db2db.biodbnet.services.settings.user_cache_dir
        database_file = os.path.join(database_dir, "async_biodbnet.db")
        instance.connection = await aiosqlite.connect(database_file)
        
        await instance.connection.execute(f"""
        CREATE TABLE IF NOT EXISTS {instance._table_name}(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            taxon_id INTEGER
        );
        """)
        await instance.connection.commit()
        
        return instance
    
    async def close(self):
        if self.connection:
            await self.connection.close()
    
    async def _add_columns(self, columns: List[str]):
        cursor: Cursor = await self.connection.execute(f"PRAGMA table_info({self._table_name})")
        columns_in_db: List[str] = [i[1] for i in await cursor.fetchall()]
        await cursor.close()
        for column in columns:
            if column not in self._db_columns:
                self._db_columns.append(column)
            
            if column not in columns_in_db:
                await self.connection.execute(f"ALTER TABLE {self._table_name} ADD COLUMN {column} TEXT")
                await self.connection.commit()
    
    async def _get_from_cache(self, input_db: str, output_db: list[str], value: str, taxon_id: int) -> pd.DataFrame:
        """
        This function will get the row from the database under the column "input_db" where the value is "value"
        :return:
        """
        select_columns: list[str] = [input_db] + output_db
        cursor: Cursor = await self.connection.execute(
            f"SELECT {', '.join(select_columns)} FROM {self._table_name} WHERE taxon_id=? AND {input_db}=?",
            (taxon_id, value)
        )
        row = await cursor.fetchall()
        await cursor.close()
        
        df: DataFrame = pd.DataFrame(row, columns=select_columns)
        
        if df.empty:
            # If the dataframe is empty, set the following:
            # taxon_id: taxon_id
            # input_db: value
            # Remaining values: pd.NA
            # *[pd.NA] * (len(df.columns) - 2]: The number of columns minus 2 (taxon_id, `input_db`)
            df.loc[0] = [value, *[pd.NA] * (len(df.columns) - 1)]
        
        return df
    
    async def _add_to_cache(self, df: pd.DataFrame, taxon_id: int):
        # Get the current columns of the dataframe
        
        # Make columns lowercase
        df.columns = [i.replace(" ", "_").lower() for i in df.columns]
        db_columns = ["taxon_id"] + list(df.columns)
        
        # Create a new column to determine which rows already exist in the database and should be updated
        df["exists"] = False
        index: int
        row: pd.Series
        for index, row in df.iterrows():
            # First, find if the row exists in the database. Search by taxon_id and db_columns[0]
            cursor: Cursor = await self.connection.execute(
                f"SELECT 1 FROM {self._table_name} WHERE taxon_id=? AND {db_columns[1]}=?",
                (taxon_id, row[db_columns[1]])
            )
            row_exists = await cursor.fetchall()  # Will be `1` if the row exists, otherwise None
            await cursor.close()
            
            if row_exists:
                df.loc[index, "exists"] = True
        
        insert_df = df[df["exists"] == False].copy()
        insert_df.drop(columns=["exists"], inplace=True)
        insert_values = [(taxon_id, *row.values.tolist()) for index, row in insert_df.iterrows()]
        
        update_df = df[df["exists"] == True].copy()
        update_df.drop(columns=["exists"], inplace=True)
        update_values = [(taxon_id, *row.values.tolist()) for index, row in update_df.iterrows()]
        
        insert_command = f"INSERT INTO {self._table_name} ({', '.join(db_columns)}) VALUES ({', '.join(['?'] * len(db_columns))})"
        update_command = f"UPDATE {self._table_name} SET {', '.join([f'{i}=?' for i in db_columns[1:]])} WHERE taxon_id=? AND {db_columns[1]}=?"
        
        await self.connection.executemany(insert_command, insert_values)
        await self.connection.executemany(update_command, update_values)
        
        await self.connection.commit()
    
    async def get(
        self,
        input_values: List[str],
        input_db: str,
        output_db: List[str],
        taxon_id: int,
    ) -> pd.DataFrame:
        
        sanitize_input_db = input_db.replace(" ", "_").lower()
        sanitize_output_db = [i.replace(" ", "_").lower() for i in output_db]
        columns_to_return = [sanitize_input_db] + sanitize_output_db
        cache_df = pd.DataFrame(columns=[sanitize_input_db] + sanitize_output_db)
        
        if self.cache:
            await self._add_columns([sanitize_input_db] + sanitize_output_db)
            for item in input_values:
                row_df: pd.DataFrame = await self._get_from_cache(sanitize_input_db, sanitize_output_db, item, taxon_id)
                cache_df = pd.concat([cache_df, row_df], ignore_index=True)
            not_in_cache: pd.DataFrame = cache_df[cache_df[sanitize_output_db].apply(lambda x: x.isna().any(), axis=1)]
        else:
            not_in_cache = pd.DataFrame()
            not_in_cache[sanitize_input_db] = input_values
        
        # Get input_values not found in df[sanitize_output_db] columns
        
        if not not_in_cache.empty:
            conversion_items = not_in_cache[sanitize_input_db].tolist()
            conversion: pd.DataFrame = await asyncio.to_thread(
                self.biodbnet.db2db,
                input_values=conversion_items,
                input_db=input_db,
                output_db=output_db,
                taxon=taxon_id
            )
            conversion.reset_index(inplace=True)
            conversion.columns = [i.replace(" ", "_").lower() for i in conversion.columns]
            
            if self.cache:
                await self._add_to_cache(conversion.copy(), taxon_id)
            
            cache_df = cache_df[~cache_df[sanitize_input_db].isin(conversion_items)]
            cache_df = pd.concat([cache_df, conversion], ignore_index=True)
        
        cache_df.reset_index(inplace=True, drop=True)
        cache_df = cache_df[cache_df[sanitize_input_db].isin(input_values)]
        cache_df = cache_df[columns_to_return]
        
        changed_columns = cache_df.columns.tolist()
        changed_columns[0] = input_db
        changed_columns[1:] = output_db
        cache_df.columns = changed_columns
        
        return cache_df


async def _execute_db2db(
    biodbnet: _db2db,
    input_values: List[str],
    input_db: str,
    output_db: List[str],
    taxon_id: int,
    delay: int = 10,
) -> pd.DataFrame:
    conversion: pd.DataFrame = await biodbnet.get(
        input_values=input_values,
        input_db=input_db,
        output_db=output_db,
        taxon_id=taxon_id
    )
    
    # If the above db2db conversion didn't work, try again until it does
    if not isinstance(conversion, pd.DataFrame):
        # Errors will occur on a timeout. If this happens, split our working dataset in two and try again
        first_set: List[str] = input_values[:len(input_values) // 2]
        second_set: List[str] = input_values[len(input_values) // 2:]
        
        await asyncio.sleep(delay)
        first_conversion: pd.DataFrame = await biodbnet.get(
            input_values=first_set,
            input_db=input_db,
            output_db=output_db,
            taxon_id=taxon_id
        )
        second_conversion: pd.DataFrame = await biodbnet.get(
            input_values=second_set,
            input_db=input_db,
            output_db=output_db,
            taxon_id=taxon_id
        )
        
        return pd.concat([first_conversion, second_conversion])
    
    return conversion


async def _worker(
    queue: asyncio.Queue,
    result_queue: asyncio.Queue,
    num_items: int,
    num_collected: Value,
    quiet: bool
):
    if not quiet:
        print("\rCollecting genes...", end="")
    
    while not queue.empty():
        item = await queue.get()
        db2db_result = await item
        await result_queue.put(db2db_result)
        
        num_collected.value += len(db2db_result)
        if not quiet:
            print(f"\rCollecting genes... {num_collected.value} of {num_items} finished", end="")
        
        queue.task_done()


async def db2db(
    input_values: Union[List[str], List[int]],
    input_db: InputDatabase,
    output_db: Union[OutputDatabase, Iterable[OutputDatabase]] = (
        OutputDatabase.GENE_SYMBOL.value,
        OutputDatabase.GENE_ID.value,
        OutputDatabase.CHROMOSOMAL_LOCATION.value
    ),
    taxon_id: Union[TaxonID, int] = TaxonID.HOMO_SAPIENS,
    quiet: bool = False,
    remove_duplicates: bool = False,
    delay: int = 5,
    concurrency: int = 8,
    batch_length: int = 300,
    async_cache: bool = True,
    biodbnet_cache: bool = False
) -> pd.DataFrame:
    """
    Convert gene information using BioDBNet

    :param input_values: A list of genes in "input_db" format
    :param input_db: The input database to use (default: "Ensembl Gene ID")
    :param output_db: The output format to use (default: ["Gene Symbol", "Gene ID", "Chromosomal Location"])
    :param delay: The delay in seconds to wait before trying again if bioDBnet is busy (default: 15)
    :param taxon_id: The taxon ID to use (default: 9606)
    :param quiet: Should the conversions show output or not?
    :param remove_duplicates: Should duplicate values be removed from the resulting dataframe?
    :param concurrency: The number of concurrent connections to make to BioDBNet
    :param batch_length: The maximum number of items to convert at a time
    :param async_cache: Should the cache be used? (default: True)
    :param biodbnet_cache: Should the BioDBNet cache be used? (default: False)
    
    :return: A dataframe with specified columns as "output_db" (Default is HUGO symbol, Entrez ID, and chromosome start and end positions)
    """
    input_values: List[str] = [str(i) for i in input_values]
    input_db_value: str = input_db.value
    
    output_db_values: List[str]
    if isinstance(output_db, OutputDatabase):
        output_db_values = [output_db.value]
    else:
        output_db_values = [str(i.value) for i in output_db]
    
    # Check if input_db_value is in output_db_values
    if input_db_value in output_db_values:
        raise ValueError("Input database cannot be in output database")
    
    if isinstance(taxon_id, TaxonID):
        taxon_id_value: int = int(taxon_id.value)
    else:
        taxon_id_value: int = int(taxon_id)
    
    # Validate input settings
    if concurrency > 20:
        raise ValueError(f"Concurrency cannot be greater than 20. {concurrency} was given.")
    
    if batch_length > 500 and taxon_id_value == TaxonID.HOMO_SAPIENS.value:
        raise ValueError(f"Batch length cannot be greater than 500 for Homo Sapiens. {batch_length} was given.")
    elif batch_length > 300 and taxon_id_value == TaxonID.MUS_MUSCULUS.value:
        raise ValueError(f"Batch length cannot be greater than 300 for Mus Musculus. {batch_length} was given.")
    
    if async_cache and biodbnet_cache:
        raise ValueError(
            f"Only one cache system may be used: async_cache or biodbnet_cache. Received `True` for both cache systems.")
    
    biodbnet = await _db2db.init(quiet=quiet, async_cache=async_cache, biodbnet_cache=biodbnet_cache)
    biodbnet.biodbnet.services.TIMEOUT = 60
    
    # Define variables
    # Create queues to hold results
    queue: asyncio.Queue = asyncio.Queue()
    result_queue: asyncio.Queue = asyncio.Queue()
    # Hold number of items complete
    num_collected: Value = Value('i', 0)
    
    # Create tasks to be completed
    for i in range(0, len(input_values), batch_length):
        # Define an upper range of values to take from input_values
        upper_range = min(i + batch_length, len(input_values))
        task = _execute_db2db(
            biodbnet=biodbnet,
            input_values=input_values[i:upper_range],
            input_db=input_db_value,
            output_db=output_db_values,
            taxon_id=taxon_id_value,
            delay=delay
        )
        queue.put_nowait(task)
    
    workers = [
        asyncio.create_task(_worker(
            queue=queue,
            result_queue=result_queue,
            num_items=len(input_values),
            num_collected=num_collected,
            quiet=quiet,
        ))
        for _ in range(concurrency)
    ]
    
    await asyncio.gather(*workers)  # Start work
    await queue.join()  # Wait for work to complete
    await biodbnet.close()
    # Work is complete and workers are done. Cancel them
    for w in workers:
        w.cancel()
    
    # Collect results from result_queue
    conversion_results = []
    while not result_queue.empty():
        conversion_results.append(await result_queue.get())
    
    if not quiet:
        print("")
    main_df: pd.DataFrame = pd.DataFrame()
    item: pd.DataFrame
    for i, item in enumerate(conversion_results):
        main_df = pd.concat([main_df, item])
        if not quiet:
            print(f"Concatenating dataframes... {i + 1} of {len(conversion_results)}" + " " * 50, end="\r")
    
    if not quiet:
        print("")
    
    # Remove duplicate index values
    if remove_duplicates:
        main_df = main_df[~main_df.index.duplicated(keep='first')]
    
    # Move index to column
    
    main_df.reset_index(inplace=True, drop=True)
    return main_df


async def runner():
    db_path = "/Users/joshl/Library/Caches/bioservices/async_biodbnet.db"
    table_name = "db2db"
    async with aiosqlite.connect(db_path) as db:
        await db.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name}(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                taxon_id INTEGER,
                gene_id TEXT,
                gene_symbol TEXT
            );
        """)
        
        await db.execute(
            f"INSERT INTO {table_name} (taxon_id, gene_id, gene_symbol) VALUES (?,?,?)",
            (9096, "1", "123")
        )
        await db.execute(
            f"INSERT INTO {table_name} (taxon_id, gene_id, gene_symbol) VALUES (?,?,?)",
            (9096, "4", "456")
        )
        await db.execute(
            f"INSERT INTO {table_name} (taxon_id, gene_id, gene_symbol) VALUES (?,?,?)",
            (9096, "7", "789")
        )
        await db.commit()
        
        # Print all items in the database
        cursor = await db.execute(f"SELECT * FROM {table_name}")
        rows = await cursor.fetchall()
        await cursor.close()
        print(rows)


if __name__ == "__main__":
    # asyncio.run(runner())
    df = asyncio.run(db2db(
        input_values=["14910", "22059", "11816", "21898"],  # [str(i) for i in range(1000, 2000)],
        input_db=InputDatabase.GENE_ID,
        output_db=[OutputDatabase.GENE_SYMBOL],
        taxon_id=TaxonID.MUS_MUSCULUS,
        quiet=False,
        async_cache=True,
        biodbnet_cache=False
    ))
    
    print(df.values.tolist())
    # print(df[df["Gene ID"] == "1"]["Gene Symbol"].values[0] == "A1BG")
    # print(df[df["Gene ID"] == "2"]["Gene Symbol"].values[0] == "A2M")
    # print(df[df["Gene ID"] == "3"]["Gene Symbol"].values[0] == "A2MP1")
    # print(df[df["Gene ID"] == "4"]["Gene Symbol"].values[0] == "-")
