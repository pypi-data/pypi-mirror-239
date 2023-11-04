import xml.etree.ElementTree as ET
import datetime, requests, re

StopColumns = {
    'SDURAKKODU'     : 'StopCode',
    'SDURAKADI'      : 'StopName',
    'KOORDINAT'      : 'KOORDINAT',
    'ILCEADI'        : 'District',
    'SYON'           : 'Direction',
    'AKILLI'         : 'IsSmart',
    'FIZIKI'         : 'PhysicalCondition',
    'DURAK_TIPI'     : 'Type',
    'ENGELLIKULLANIM': 'Accessibility'
    }

GarageColumns = {
    'ID'        : 'GarageId',
    'GARAJ_ADI' : 'GarageName',
    'GARAJ_KODU': 'GarageCode',
    'KOORDINAT' : 'KOORDINAT'
    }

AnnouncementColumns = {
    'HATKODU'         : 'LineCode',
    'HAT'             : 'LineName',
    'TIP'             : 'Type',
    'GUNCELLEME_SAATI': 'UpdateTime',
    'MESAJ'           : 'Message'
    }

BadRoadColums = {
    'NMESAJID'     : 'MessageId',
    'SKAPINUMARASI': 'BusId',
    'SSOFORSICILNO': 'DriveId',
    'SMESAJMETNI'  : 'Message',
    'DTKAYITZAMANI': 'UpdateDate',
    'NBOYLAM'      : 'Longitude',
    'NENLEM'       : 'Latitude'
    }

AccidentColums = {
    'DTOLAYBASLANGICZAMANI': 'AccidentDate',
    'NBOYLAM'              : 'Longitude',
    'NENLEM'               : 'Latitude',
    'Tur'                  : 'Type',
    }

LineStopColums = {
    'HATKODU'        : 'LineCode',
    'YON'            : 'Direction',
    'SIRANO'         : 'SequenceNo',
    'DURAKKODU'      : 'StopCode',
    'DURAKADI'       : 'StopName',
    'XKOORDINATI'    : 'Longitude',
    'YKOORDINATI'    : 'Latitude',
    'DURAKTIPI'      : 'Type',
    'ISLETMEBOLGE'   : 'BusinessRegion',
    'ISLETMEALTBOLGE': 'SubRegion',
    'ILCEADI'        : 'District'
    }

LineDetailColumns = {
    'HAT_KODU'    : 'LineCode',
    'HAT_ADI'     : 'LineName',
    'TAM_HAT_ADI' : 'LineFullName',
    'HAT_DURUMU'  : 'LineStatus',
    'BOLGE'       : 'BusinessRegion',
    'SEFER_SURESI': 'TravelTime'
    }

def GetStopByCode(stopCode):
    url = "https://api.ibb.gov.tr/iett/UlasimAnaVeri/HatDurakGuzergah.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/GetDurak_XML",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                   <Body>
                       <GetDurak_XML xmlns="http://tempuri.org/">
                           <DurakKodu>{stopCode}</DurakKodu>
                       </GetDurak_XML>
                   </Body>
               </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()

    root = ET.fromstring(r.content)
    if table := root.findall('*//Table'):
        table = {StopColumns[it.tag]: it.text for it in table[0].iter() if it.text}
        if coords := table.pop('KOORDINAT', None):
            pattern = r'POINT\s\((?P<Longitude>.*)\s(?P<Latitude>.*)\)'
            if matches := re.match(pattern, coords):
                table.update({key: float(value) for key, value in matches.groupdict().items()})
        return table
    return None

def GetAllGarages():
    url = "https://api.ibb.gov.tr/iett/UlasimAnaVeri/HatDurakGuzergah.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/GetGaraj_XML",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                  <Body>
                      <GetGaraj_XML xmlns="http://tempuri.org/"/>
                  </Body>
              </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    
    root = ET.fromstring(r.content)
    if tables := root.findall('*//Table'):
        results = []
        for table in tables:
            table = {GarageColumns[it.tag]: it.text for it in table.iter() if it.text}
            if coords := table.pop('KOORDINAT', None):
                pattern = r'POINT\s\((?P<Longitude>.*)\s(?P<Latitude>.*)\)'
                if matches := re.match(pattern, coords):
                    table.update()
            results.append(table)
        return results
    return None

def GetAnnouncements():
    url = "https://api.ibb.gov.tr/iett/UlasimDinamikVeri/Duyurular.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/GetDuyurular_XML",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                  <Body>
                      <GetDuyurular_XML xmlns="http://tempuri.org/"/>
                  </Body>
              </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    
    root = ET.fromstring(r.content)
    if tables := root.findall('*//Table'):
        results = []
        for table in tables:
            table = {AnnouncementColumns[it.tag]: it.text for it in table.iter() if it.text}
            if updateTime := table.get('UpdateTime'):
                pattern = r'Kayit Saati: \d{2}:\d{2}'
                if matches := re.match(pattern, updateTime):
                    updateTime = updateTime.replace('Kayit Saati: ', '')
                    table['UpdateTime'] = updateTime
            results.append(table)
        return results
    return None

def GetBadRoads():
    url = "https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/GetBozukSatih_XML",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = """<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                  <Body>
                      <GetBozukSatih_XML xmlns="http://tempuri.org/"/>
                  </Body>
              </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    
    root = ET.fromstring(r.content)
    if tables := root.findall('*//Table'):
        results = []
        for table in tables:
            table = {BadRoadColums[it.tag]: it.text for it in table.iter() if it.text}
            table.update({
                'Longitude': float(table['Longitude']),
                'Latitude': float(table['Latitude'])
                })
            results.append(table)
        return results
    return None

def GetAccidentsByDate(dt):
    url = "https://api.ibb.gov.tr/iett/FiloDurum/SeferGerceklesme.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/GetKazaLokasyon_XML",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                   <Body>
                       <GetKazaLokasyon_XML xmlns="http://tempuri.org/">
                           <Tarih>{dt:%Y-%m-%d}</Tarih>
                       </GetKazaLokasyon_XML>
                   </Body>
               </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    
    root = ET.fromstring(r.content)
    if tables := root.findall('*//Table'):
        results = []
        for table in tables:
            table = {AccidentColums[it.tag]: it.text for it in table.iter() if it.text}
            table.update({
                'Longitude': float(table['Longitude']),
                'Latitude': float(table['Latitude'])
                })
            results.append(table)
        return results
    return None

def GetLineStopsByCode(lineCode):
    url = "https://api.ibb.gov.tr/iett/ibb/ibb.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/DurakDetay_GYY",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                   <Body>
                       <DurakDetay_GYY xmlns="http://tempuri.org/">
                           <hat_kodu>{lineCode}</hat_kodu>
                       </DurakDetay_GYY>
                   </Body>
               </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()
    
    root = ET.fromstring(r.content)
    if tables := root.findall('*//Table'):
        results = []
        for table in tables:
            table = {LineStopColums[it.tag]: it.text for it in table.iter() if it.text}
            table.update({
                'Longitude': float(table['Longitude']),
                'Latitude': float(table['Latitude'])
                })
            results.append(table)
        return results
    return None

def GetLineDetails(lineCode):
    url = "https://api.ibb.gov.tr/iett/ibb/ibb.asmx"
    headers = {
        "SOAPAction": "http://tempuri.org/HatServisi_GYY",
        "Content-type": "text/xml;charset=utf-8"
        }
    data = f"""<Envelope xmlns="http://schemas.xmlsoap.org/soap/envelope/">
                   <Body>
                       <HatServisi_GYY xmlns="http://tempuri.org/">
                           <hat_kodu>{lineCode}</hat_kodu>
                       </HatServisi_GYY>
                   </Body>
               </Envelope>"""
    r = requests.post(url, data=data, headers=headers)
    r.raise_for_status()

    root = ET.fromstring(r.content)
    if table := root.findall('*//Table'):
        table = {LineDetailColumns[it.tag]: it.text for it in table[0].iter() if it.text}
        return table
    return None







