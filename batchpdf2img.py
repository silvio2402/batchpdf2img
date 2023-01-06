import os
import argparse
import glob
import pdf2image
from pdf2image.generators import threadsafe
import threading
import queue
import time


def convert_pdfs_thread(doc_queue: queue.Queue, output_dir: str, format: str, overwrite: bool):
    while True:
        try:
            doc_i, doc_path = doc_queue.get_nowait()
        except queue.Empty:
            return

        # check if whole pdf already converted
        if not overwrite:
            info = pdf2image.pdfinfo_from_path(doc_path)
            last_page = int(info["Pages"])
            filename = f"{str(doc_i).rjust(4, '0')}-{last_page}.{format}"
            if os.path.exists(os.path.join(output_dir, filename)):
                continue

        @threadsafe
        def generator():
            while True:
                yield str(doc_i).rjust(4, "0")

        print(f"\nConverting {doc_path}")
        pdf2image.convert_from_path(doc_path, dpi=200, output_folder=output_dir,
                                    paths_only=True, output_file=generator(), fmt=format)

        doc_queue.task_done()


def convert_pdfs(doc_path_wildcard: str, output_dir: str, format: str, overwrite: bool, max_threads: int):
    doc_paths = glob.glob(doc_path_wildcard, recursive=True)
    doc_amount = len(doc_paths)

    doc_queue = queue.Queue()
    [doc_queue.put(doc) for doc in enumerate(doc_paths)]

    threads = []

    # Spawn threads
    for _ in range(min(max_threads, doc_amount)):
        thread = threading.Thread(target=convert_pdfs_thread, args=(
            doc_queue, output_dir, format, overwrite))
        thread.start()
        threads.append(thread)

    def join():
        while min([thread.is_alive() for thread in threads]) == True:
            time.sleep(1)

    return doc_queue, doc_amount, join


def main(doc_path_wildcard: str, output_dir: str, format: str, overwrite: bool, max_threads: int):
    doc_queue, doc_amount, join = convert_pdfs(
        doc_path_wildcard, output_dir, format, overwrite, max_threads)

    def progress_thread(exit_event: threading.Event):
        while True:
            try:
                size = doc_queue.qsize()
                print(f"{doc_amount-size}/{doc_amount}", end="\r")
                time.sleep(1)
                if exit_event.is_set():
                    return
            except KeyboardInterrupt:
                return

    p_exit_event = threading.Event()
    p_thread = threading.Thread(target=progress_thread, args=(p_exit_event,))
    p_thread.start()

    # Wait for all threads to finish
    join()

    p_exit_event.set()

    print("\nDone")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="batch convert pdfs to images")
    parser.add_argument("files", help="input files wildcard", type=str)
    parser.add_argument(
        "-o", "--output", help="output directory", required=True)
    parser.add_argument(
        "-e", "--ext", help="output format extension", default="png")
    parser.add_argument("-t", "--max-threads",
                        help="max number of converter threads", type=int, default=10)
    parser.add_argument("-w", "--overwrite", help="overwrite all document, else only incomplete",
                        action='store_true', default=False)
    args = parser.parse_args()

    main(args.files, args.output, args.ext, args.max_threads, args.overwrite)
