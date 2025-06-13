from decoder import decode_adsb_message
import os


def read_sample_data(file_path):

    if not os.path.exists(file_path):
        print(f"errror:{file_path} not forund")
        return []
    
    with open(file_path,'r') as file:
        clean_lines=[]
        for line in file:
            stripped_line=line.strip()
            if stripped_line:
                clean_lines.append(stripped_line)
        return clean_lines
    

def main():
    data_file='sample_data.txt'
    messages=read_sample_data(data_file)

    if not messages:
        print('nodata to decode')
        return
    
    for msg in messages:
        try:
            result=decode_adsb_message(msg)
            if result:
                print(result)
        except Exception as e:
            print(f'error decoding message {msg}: {e}')


if __name__ == "__main__":
    main()