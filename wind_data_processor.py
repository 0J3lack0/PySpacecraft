import xlrd
import xlwt
import itertools

readBook        = xlrd.open_workbook('wind_data.xlsx')
writeBook       = xlwt.Workbook()
sheetRowCounter = {}
refs            = []

def get_sheet_by_name(book, name):
    try:
        for idx in itertools.count():
            sheet = book.get_sheet(idx)
            if sheet.name == name:
                return sheet
    except IndexError:
        return None

def find_doy(sheet, ref):
    return sheet.cell_value(ref[1] + 1, ref[2] - 1)

def find_n2ref(sheet, ref):
    return sheet.cell_value(ref[1] + 1, ref[2])

def find_min_max_ref_row(sheet, ref, n2Ref):
    for i in range(5, 374):
        if sheet.cell_value(i, ref[2] - 1) > n2Ref:
            return (i - 1, i)

def calculate_avg_mach(sheet, ref, n2Ref, minRefRow, maxRefRow):
    minMach = (sheet.cell_value(minRefRow, ref[2] - 1) * sheet.cell_value(minRefRow, 1)) / n2Ref
    maxMach = (sheet.cell_value(maxRefRow, ref[2] - 1) * sheet.cell_value(maxRefRow, 1)) / n2Ref

    return (minMach + maxMach) / 2

def calculate_m2_div_m1(sheet, ref, minRefRow, mach):
    minMach    = sheet.cell_value(minRefRow, 1)
    minM2DivM1 = sheet.cell_value(minRefRow, 3)

    return (mach * minM2DivM1) / minMach

def calculate_m2(sheet, ref, minRefRow, mach):
    minMach = sheet.cell_value(minRefRow, 1)
    minM2   = sheet.cell_value(minRefRow, 4)

    return (mach * minM2) / minMach

def calculate_kappa_1(sheet, ref, minRefRow, mach):
    minMach   = sheet.cell_value(minRefRow, 1)
    minKappa1 = sheet.cell_value(minRefRow, 5)

    return (mach * minKappa1) / minMach

def calculate_u2_div_u1(sheet, ref, minRefRow, mach):
    minMach    = sheet.cell_value(minRefRow, 1)
    minU2DivU1 = sheet.cell_value(minRefRow, 6)

    return (mach * minU2DivU1) / minMach

def calculate_cs2_div_cs1(sheet, ref, minRefRow, mach):
    minMach      = sheet.cell_value(minRefRow, 1)
    minCS2DivCS1 = sheet.cell_value(minRefRow, 8)

    return (mach * minCS2DivCS1) / minMach

def calculate_n2(sheet, ref, minRefRow, mach):
    minMach = sheet.cell_value(minRefRow, 1)
    minN2   = sheet.cell_value(minRefRow, 9)

    return (mach * minN2) / minMach

def calculate_u2(sheet, ref, minRefRow, mach):
    minMach = sheet.cell_value(minRefRow, 1)
    minU2   = sheet.cell_value(minRefRow, 10)

    return (mach * minU2) / minMach

def calculate_data(sheet, ref, n2Ref):
    data  = {
        'DOY': find_doy(sheet, ref),
        'Mach': '',
        'M2/M1': '',
        'M2': '',
        'Kappa_1': '',
        'U2/U1': '',
        'cs2^2/cs1^2': '',
        'n1': '',
        'u1': '',
        'n2': '',
        'u2': ''
    }

    minN2 = sheet.cell_value(ref[1] + 5, ref[2] - 1)
    maxN2 = sheet.cell_value(ref[1] + 374, ref[2] - 1)

    if n2Ref < minN2:
        data['Mach']        = '1.1500'
        data['M2/M1']       = '0.76312'
        data['M2']          = '0.8775852677'
        data['Kappa_1']     = '1.22383'
        data['U2/U1']       = '0.81711'
        data['cs2^2/cs1^2'] = '1.14650'
        data['n1']          = sheet.cell_value(ref[1] + 3, ref[2] - 1)
        data['u1']          = sheet.cell_value(ref[1] + 3, ref[2])
        data['n2']          = sheet.cell_value(ref[1] + 5, ref[2] - 1)
        data['u2']          = sheet.cell_value(ref[1] + 5, ref[2])

    elif n2Ref > maxN2:
        data['Mach']        = '5000'
        data['M2/M1']       = '0'
        data['M2']          = '0'
        data['Kappa_1']     = '0'
        data['U2/U1']       = '0'
        data['cs2^2/cs1^2'] = '0'
        data['n1']          = '0'
        data['u1']          = '0'
        data['n2']          = '0'
        data['u2']          = '0'

    else:
        minRefRow, maxRefRow = find_min_max_ref_row(sheet, ref, n2Ref)
        data['Mach']         = calculate_avg_mach(sheet, ref, n2Ref, minRefRow, maxRefRow)
        data['M2/M1']        = calculate_m2_div_m1(sheet, ref, minRefRow, data['Mach'])
        data['M2']           = calculate_m2(sheet, ref, minRefRow, data['Mach'])
        data['Kappa_1']      = calculate_kappa_1(sheet, ref, minRefRow, data['Mach'])
        data['U2/U1']        = calculate_u2_div_u1(sheet, ref, minRefRow, data['Mach'])
        data['cs2^2/cs1^2']  = calculate_cs2_div_cs1(sheet, ref, minRefRow, data['Mach'])
        data['n1']           = sheet.cell_value(ref[1] + 3, ref[2] - 1)
        data['u1']           = sheet.cell_value(ref[1] + 3, ref[2])
        data['n2']           = calculate_n2(sheet, ref, minRefRow, data['Mach'])
        data['u2']           = calculate_u2(sheet, ref, minRefRow, data['Mach'])

    return data

for sheet in readBook.sheets():
    sheetRowCounter[sheet.name] = 0
    writeSheet = writeBook.add_sheet(sheet.name)
    writeSheet.write(0, 0, 'DOY')
    writeSheet.write(1, 0, 'Mach')
    writeSheet.write(2, 0, 'M2/M1')
    writeSheet.write(3, 0, 'M2')
    writeSheet.write(4, 0, 'Kappa_1')
    writeSheet.write(5, 0, 'U2/U1')
    writeSheet.write(6, 0, 'cs2^2/cs1^2')
    writeSheet.write(7, 0, 'n1')
    writeSheet.write(8, 0, 'u1')
    writeSheet.write(9, 0, 'n2')
    writeSheet.write(10, 0, 'u2')

    for rowID in range(sheet.nrows):
        row = sheet.row(rowID)
        for colID, cell in enumerate(row):
            if cell.value == "n2ref" :
                refs.append([sheet.name, rowID, colID])

for ref in refs:
    readSheet                = readBook.sheet_by_name(ref[0])
    n2Ref                    = find_n2ref(readSheet, ref)
    calculatedData           = calculate_data(readSheet, ref, n2Ref)
    writeSheet               = get_sheet_by_name(writeBook, ref[0])
    sheetRowCounter[ref[0]] += 1

    writeSheet.write(0, sheetRowCounter[ref[0]], calculatedData['DOY'])
    writeSheet.write(1, sheetRowCounter[ref[0]], calculatedData['Mach'])
    writeSheet.write(2, sheetRowCounter[ref[0]], calculatedData['M2/M1'])
    writeSheet.write(3, sheetRowCounter[ref[0]], calculatedData['M2'])
    writeSheet.write(4, sheetRowCounter[ref[0]], calculatedData['Kappa_1'])
    writeSheet.write(5, sheetRowCounter[ref[0]], calculatedData['U2/U1'])
    writeSheet.write(6, sheetRowCounter[ref[0]], calculatedData['cs2^2/cs1^2'])
    writeSheet.write(7, sheetRowCounter[ref[0]], calculatedData['n1'])
    writeSheet.write(8, sheetRowCounter[ref[0]], calculatedData['u1'])
    writeSheet.write(9, sheetRowCounter[ref[0]], calculatedData['n2'])
    writeSheet.write(10, sheetRowCounter[ref[0]], calculatedData['u2'])

writeBook.save('wind_data_calculated.xlsx')