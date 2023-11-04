import argparse

from funread.legado.task import GenerateSourceTask
from funread.legado.task import ReadODSProgressDataTask
from funread.legado.task import ReadODSSourceDataTask
from funread.legado.task import ReadODSUrlDataTask
from funread.legado.task import UpdateRssTask


# ReadODSUrlDataTask().run()
# ReadODSSourceDataTask().run()
# ReadODSProgressDataTask().run()
# GenerateSourceTask().run()
#GenerateSourceTask().update_rss()
#UpdateRssTask().run()
#UpdateRssTask().update_main()

from fundrive import GithubDrive
drive = GithubDrive()
drive.login("farfarfun/funread-cache")
data=drive.get_file_info('funread/legado/book/snapshot/20231011/index.html')
print(data)