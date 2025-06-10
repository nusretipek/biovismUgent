from freezerConfig import freezer
import shutil

if __name__ == '__main__':
    freezer.freeze()
    shutil.copyfile('app/templates/404.html', 'app/build/404.html')

