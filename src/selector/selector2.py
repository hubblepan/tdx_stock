# -*- coding:utf-8 -*-
import src.stock_io as sio
from src.StockIndicator import max_zf, _sma,red_bar
import numpy as np
from src.terminate import remove_duplicate_zxg


def remove_duplicate(path = 'C:\\new_tdx\\T0002\\blocknew\\ZXG.blk'):
    result = []
    with open(path, mode='r') as f:
        for line in f.readlines():
            if not '\n' == line and line != '':
                if line.strip('\n') not in result:
                    result.append(line.strip('\n'))
    with open(path, mode='w') as f:
        for stock_code in result:
            f.write(stock_code)
            f.write('\n')
    return  result

def main(position=-1, plate='sh'):
    if plate == 'sh':
        code_list = sio.get_stock_code_list(sio.dir_day_sh)
    elif plate == 'sz':
        code_list = sio.get_stock_code_list(sio.dir_day_sz)
    else:
        print('error: plate parameter error')
        return
    print(code_list)
    result = []

    for stock_code in code_list:
        try:
            kline = sio.load_stock(stock_code, plate=plate)
            zf = max_zf(kline)
            if position != -1:
                _open = kline['open'][position-9: position + 1].astype('float')
                close = kline['close'][position-9: position + 1].astype('float')
                vol = kline['vol'][position-9: position + 1].astype('float')
                amount = kline['amount'][position-9: position + 1].astype('float')
                ratio = kline['ratio'][position-9: position + 1].astype('float')
                sma_close_5 = _sma(np.array(kline['close'].astype('float')), 5)[position - 9: position + 1]
                sma_vol_10 = _sma(np.array(kline['vol'].astype('float')), 10)[position - 9: position + 1]
                sma_amount_10 = _sma(np.array(kline['vol'].astype('float')), 10)[position - 9: position + 1]
                entity = red_bar(kline)[position - 9: position + 1]
            else:
                _open = kline['open'][position - 9: ].astype('float')
                close = kline['close'][position - 9: ].astype('float')
                vol = kline['vol'][position - 9: ].astype('float')
                amount = kline['amount'][position - 9:].astype('float')
                ratio = kline['ratio'][position - 9:].astype('float')
                sma_close_5 = _sma(np.array(kline['close'].astype('float')), 5)[position - 9: ]
                sma_vol_10 = _sma(np.array(kline['vol'].astype('float')), 10)[position - 9: ]
                sma_amount_10 = _sma(np.array(kline['vol'].astype('float')), 10)[position - 9: ]
                entity = red_bar(kline)[position - 9: ]

            if vol[-1] > sma_vol_10[-2] * 1.1 and vol[-1] > np.max(vol[-6:-1]) and _open[-1] < sma_close_5[-1] < close[-1]:
                if sma_amount_10[-2] * 10 > 150000000:
                    if entity[-1] > 4 and close[-1] > _open[-1]:
                        result.append(stock_code)
                        print(stock_code)
        except Exception as e:
            pass

    print(len(result))
    with open('C:\\new_tdx\T0002\\blocknew\\ZXG.blk', mode='a') as f:
        for stock_code in result:
            if stock_code[0] == '6':
                f.write('1'+stock_code)
            else:
                f.write('0' + stock_code)
            f.write('\n')
    with open('../data/ll.txt', mode='a') as f:
        for stock_code in result:
            if stock_code[0] == '6':
                f.write('1' + stock_code)
            else:
                f.write('0' + stock_code)
            f.write('\n')


if __name__=='__main__':
    for index in [-5, -4, -3, -2, -1]:
        main(index, plate='sh')
        main(index, plate='sz')
    remove_duplicate()


