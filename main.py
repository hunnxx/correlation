from Data import Data


def main():
    data = Data()
    data.same_processing()
    data.others_processing()
    data.write_csv('same')
    data.write_csv('others')


if __name__ == '__main__':
    main()