# -*- coding:utf-8 -*-
import src.stock_io as sio
from src.StockIndicator import max_zf

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
                vol = kline['vol'][position-9: position + 1].astype('float')
                amount = kline['amount'][position-9: position + 1].astype('float')
            else:
                vol = kline['vol'][position - 9: ].astype('float')
                amount = kline['amount'][position - 9: ].astype('float')
            max_vol = vol.max()
            if max_vol == vol[-1]:
                if amount[-1] * 10 > 150000000:
                    if zf[-1] > 4:
                        result.append(stock_code)
                        print(stock_code)
        except Exception as e:
            pass

    with open('C:\\new_tdx\T0002\\blocknew\\ZXG.blk', mode='a') as f:
        for stock_code in result:
            if stock_code[0] == '6':
                f.write('1'+stock_code)
            else:
                f.write('0' + stock_code)
            f.write('\n')


if __name__=='__main__':
    for index in [-1]:
        main(index, plate='sh')
        main(index, plate='sz')
