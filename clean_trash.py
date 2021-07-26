from pathlib import Path, PurePath
import shutil
import sys
import re
import concurrent.futures
import time
from clean_ import*
import psutil
import os
import threading


def normalize (translate_line):
   map = {ord('а'): 'a', ord('А'): 'A',
          ord('б'): 'b',ord('Б'): 'B',
          ord('в'): 'v',ord('В'): 'V',
          ord('г'): 'h',ord('Г'): 'H',
          ord('ґ'): 'g',ord('Ґ'): 'G',
          ord('д'): 'd',ord('Д'): 'D',
          ord('е'): 'e',ord('Е'): 'E',
          ord('є'): 'ie',ord('Є'): 'Ye',
          ord('ж'): 'zh',ord('Ж'): 'Zh',
          ord('з'): 'z',ord('З'): 'Z',
          ord('і'): 'i',ord('І'): 'Yi',
          ord('й'): 'i',ord('Й'): 'Y',
          ord('ї'): 'i',ord('Ї'): 'I',
          ord('и'): 'y',ord('И'): 'Y',
          ord('к'): 'k', ord('К'): 'K',
          ord('л'): 'l',ord('Л'): 'L',
          ord('м'): 'm',ord('М'): 'M',
          ord('н'): 'n',ord('Н'): 'N',
          ord('о'): 'o',ord('О'): 'O',
          ord('п'): 'p',ord('П'): 'P',
          ord('р'): 'r',ord('Р'): 'R',
          ord('с'): 's',ord('С'): 'S',
          ord('т'): 't',ord('Т'): 'T',
          ord('у'): 'u',ord('У'): 'U',
          ord('ф'): 'f',ord('Ф'): 'F',
          ord('х'): 'kh',ord('Х'): 'Kh',
          ord('ц'): 'ts',ord('Ц'): 'Ts',
          ord('ч'): 'ch',ord('Ч'): 'Ch',
          ord('ш'): 'sh',ord('Ш'): 'Sh',
          ord('щ'): 'shch',ord('Щ'): 'Shch',
          ord('ю'): 'iu',ord('Ю'): 'Yu',
          ord('я'): 'ia',ord('Я'): 'Ya',
          ord('ь'): ''}
   translated = translate_line.translate(map)
   reg = re.compile ('[^A-Za-z0-9 ]')
   return reg.sub('_',translated).strip()


def parse_file(i,path, name, counter):
   try:
      suffix = i.suffix.upper()[1:]
      f_type = 'unknown'
      for f in extensions.keys():
         if suffix in extensions[f]:
            f_type = f
            break
      if f_type == 'archives':
                   if not Path(str(path)+'\\'+f_type+'\\').exists():
                      Path(str(path)+'\\'+f_type+'\\').mkdir()
                   i = i.replace(str(path)+'\\'+name)
                   shutil.unpack_archive(str(path)+'\\'+name,
                        str(path)+'\\'+f_type+'\\'+i.stem+'\\')
                   i.unlink()          
      elif f_type == 'unknown':
         i.replace(str(path)+'\\'+name)
      else:
         if not Path(str(path)+'\\'+f_type+'\\').exists():
            Path(str(path)+'\\'+f_type+'\\').mkdir()
         i.replace(str(path)+'\\'+f_type+'\\'+name)   
   except:
      print("Unexpected error:", sys.exc_info()[0])
      print("Current path {}, counter = {}".format(i, counter))

def save_file(i, path):
   i.replace(path)

def unpack(i, path1, path2):
   shutil.unpack_archive(path1, path2)
   i.unlink()


def parse_folder(path, workers):
   try:  
      futures =[]
      thread_list=[]
      counter = 0
      with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
         for i in path.iterdir():
            name = normalize(i.stem)+i.suffix
            if i.is_dir() and i.name not in extensions.keys():
               if len(list(i.iterdir())) == 0:
                   i.rmdir()
               else:
                   i = i.replace(str(path)+'\\'+name)
                   futures.append(executor.submit(parse_folder, i, workers))                   
            else:
               parse_file(i, path, name, counter)
         for future in futures:
              future.result()
   except:
      print("Couldn't do sorting well")
      print("Unexpected error:", sys.exc_info()[0])
            

extensions = {
    'images' :  ('JPEG', 'PNG', 'JPG', 'SVG', 'TIFF', 'GIF', 'PSD', 'CDR', 'AI'),
    'video' :  ('AVI', 'MP4', 'MOV', 'MKV'),
    'documents' :  ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'PDF',
                    'XLS', 'DOCX', 'CSV', 'PPT', 'ACCDB'),
    'music': ('MP3', 'OGG', 'WAV', 'AMR'),
    'archives':  ('ZIP', 'GZ', 'TAR'),
    'python': ('PY'),
    'BIN': ('EXE', 'MSI', 'DLL')}

#testing operation speed

if __name__ == '__main__':
   print("Please let me know the path to folder you wanna be sorted: ")
   src = input()   
   dest = src + '_sorted'
   if Path(dest).exists():
      shutil.rmtree(dest)
   destination = shutil.copytree(src, dest)
   t = time.time()
   parse_folder_(Path(dest))
   print("Folder is sorted without threading in {} sec."
         .format(time.time()-t))

   for workers in range(2,5):
      shutil.rmtree(dest)
      destination = shutil.copytree(src, dest)     
      t = time.time()
      parse_folder(Path(dest), workers)
      print("Folder is sorted with max_workers param = {} in {} sec"
         .format(workers, (time.time() - t)))
   
