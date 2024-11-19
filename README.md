# pdfsplittool
split pdf tool
#git push -u origin main
#pyinstaller --onefile --noconsole --icon=app.ico my_gui_app.py


open file: open need to split file
start page: type int, must be  >  1
end page : type int must be < max pages
book mark: add index to split file, and default not add index
           And if you want to use index, and the pdf file must has index
           and must be use a compelete chapter
outputfile: special your split file name

Use this cmd to create execute program
pyinstaller --onefile --noconsole splitpdftool.py

This program no more err detect, so must input right paras

