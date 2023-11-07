from application.core.parser_data import parse_data
from application.core.jobs.get_masked_or_deleted_db import delete_rows_from_db, mask_db_chunked
from application.core.parser_data import get_all_columns_by_query


def main():
    command_line_args, conn = parse_data()
    if conn is not None:
        if command_line_args.action == 'delete':
            if command_line_args.table and command_line_args.percentage:
                confirm = input(f"{command_line_args.percentage}% of the {command_line_args.table} table will be "
                                f"deleted, do "
                                f"you confirm? (Y/N): ").lower()
                if confirm != 'n':
                    delete_rows_from_db(conn, command_line_args.table, command_line_args.percentage)
                else:
                    print("Operation canceled.")
            else:
                print("No table or percentage data to be deleted has been entered")
        elif command_line_args.action == 'mask':
            if command_line_args.table:
                if command_line_args.columns is not None:
                    confirm = input("The columns {} of the {} table will be masked, do you confirm? (Y/N): ".format(', '.join(command_line_args.columns), command_line_args.table)).lower()
                else:
                    confirm = input("All columns of the {} table will be masked, do you confirm? (Y/N): ".format(command_line_args.table)).lower()
                if confirm != 'n':
                    if not command_line_args.columns:
                        mask_db_chunked(conn, command_line_args.table,
                                        get_all_columns_by_query(command_line_args.table, conn))
                    else:
                        mask_db_chunked(conn, command_line_args.table, command_line_args.columns)
                else:
                    print("Operation canceled.")
            else:
                print("No table or columns data to be deleted has been entered")

        else:
            #   mask_db_chunked(conn, 'test_table', ['number'])
            print("Invalid Action: ", command_line_args.action)
    else:
        print('Could not connect to database')


if __name__ == "__main__":
    main()
