import logging
import sys
from readInputFile import readCarFile,readRoadFile,readCrossFile
from processFun1 import process_12 as process
from writeOutputFile import writeAnswerFile

logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))
    
    # to read input file
    car = readCarFile(car_path)
    road = readRoadFile(road_path)
    cross =  readCrossFile(cross_path)
    # process
    answer = process(car, road, cross)
    # to write output file
    writeAnswerFile(answer_path, answer)


if __name__ == "__main__":
    main()