import os
import unittest
from common.Log import MyLog as Log
import readConfig as readConfig
from common.HTMLTestRunner import HTMLTestRunner
from common.configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()


class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off
        log = Log.get_log()
        logger = log.get_logger()
        resultPath = log.get_report_path()
        on_off = localReadConfig.get_email("on_off")
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")
        self.caseFile = os.path.join(readConfig.proDir, "testCase")
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()

    def set_case_list(self):
        """
        set case list
        :return:
        """
        # 第一步打开caselist.txt，找到其中不以#开头的行，将这些行存到caseList列表中
        fb = open(self.caseListFile)
        for value in fb.readlines():
            data = str(value)
            if data != '' and not data.startswith("#"):
                # 将行保存到列表中，但是要把行末尾的换行符去掉
                self.caseList.append(data.replace("\n", ""))
        fb.close()
        print('this is test case list.')
        print(self.caseList)


    def set_case_suite(self):
        """
        set case suite
        :return:
        """
        # 调用set_case_list()方法获得要执行的用例列表，即caseList，是一个列表
        self.set_case_list()
        # 调用单元测试的TestSuite()方法，初始化一个测试套件，即test suite
        test_suite = unittest.TestSuite()
        suite_module = []

        for case in self.caseList:
            case_name = case.split("/")[-1]
            print(case_name+".py")
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            # 将找到的对应测试用例目录（caseFile）下的测试文件保存到一个列表中，即suite_module
            suite_module.append(discover)

        print('here is suite_module:')
        print(suite_module)

        if len(suite_module) > 0:
            for suite in suite_module:
                # 如果一个测试文件中包含多个测试，将其分别添加到test suite中
                for test_name in suite:
                    test_suite.addTest(test_name)
            print('here is test_suite:')
            print(test_suite)
        else:
            return None

        return test_suite

    def run(self):
        """
        run test
        :return:
        """
        try:
            # 通过set_case_suite()方法获得要执行的测试用例套件，这个套件是一个保存在用unittest.TestSuite定义的测试套件中的
            suit = self.set_case_suite()
            if suit is not None:
                # 利用Log模块记录日志信息，保存的日志文件中，即output.log
                logger.info("********TEST START********")
                # 打开执行结果文件，在执行的时候把执行结果保存到结果文件中，即report.html
                fp = open(resultPath, 'wb')
                # 利用HTMLTestRunner定义一个执行器，HTMLTestRunner是一个类似于TextTestRunner的python unittest模块的扩展
                # 第一个参数fp是报告文件report.html，第二个参数是标题，第三个参数是描述
                runner = HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                # 使用HTMLTestRunner的run方法执行测试用例套件，suit
                runner.run(suit)
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            print(str(ex))
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            fp.close()
            # send test report by email
            if on_off == 'on':
                self.email.send_email()
                logger.info("report email has been send to developer.")
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()
    obj.run()
