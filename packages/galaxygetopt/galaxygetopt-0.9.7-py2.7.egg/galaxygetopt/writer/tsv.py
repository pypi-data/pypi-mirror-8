from writer import Writer
import csv
from ..exceptions import WriterProcessingIncompleteError


class TSV(Writer):
    suffix = 'tsv'

    def process(self):
        self.processed_data = self.data
        self.processing_complete = True

    def write(self):
        if self.processing_complete:
            base_name = self.OutputFilesClass.given_filename
            if base_name is None:
                base_name = ""

            for sheet in self.processed_data:
                self.OutputFilesClass.given_filename = base_name + '.' + sheet
                self.OutputFilesClass.extension = 'tsv'
                next_output_file = self.OutputFilesClass.get_next_file()
                self.used_filenames.append(next_output_file)
                with open(next_output_file, 'wb') as csvfile:
                    tablewriter = csv.writer(csvfile, delimiter='\t', quotechar='"')
                    tablewriter.writerow(self.processed_data[sheet]['header'])
                    for row in self.processed_data[sheet]['data']:
                        tablewriter.writerow(row)
            self.OutputFilesClass.given_filename = base_name
        else:
            raise WriterProcessingIncompleteError("Write called but processing was not marked as complete. Not writing")
