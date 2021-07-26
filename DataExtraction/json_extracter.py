import requests
import csv

route = 'schools/'



service_url = 'https://services1.arcgis.com/aWQmxJWy7lM2Qqmo/arcgis/rest/services/CE_Privados3_CR/FeatureServer/0/query?where=OBJECTID+%3E+'
id_query = 0
format_url = '&outFields=*&f=json' 
last_id = 0
dependency = 'Private'
school_fragment = []
while last_id < 15248:

    response = requests.get(service_url+str(id_query)+format_url)
    jfile = response.json()
    try:
        last_id = jfile['features'][-1]['attributes']['OBJECTID']
    except Exception as e:
        print(e)
        print(jfile)
        break

    for element in jfile['features']:
        school = []
        school.append(element['attributes']['Nombre'])
        school.append(element['attributes']['Provincia'])
        school.append(element['attributes']['Canton'])
        school.append(dependency)
        if element['attributes']['TipoCE'] == '13':
            level = "Preescolar Público"
        elif element['attributes']['TipoCE'] == '10':
            level = "Escuela Pública"
        elif element['attributes']['TipoCE'] == '8':
            level = "Escuela Nocturna"
        elif element['attributes']['TipoCE'] == '5':
            level = "Colegios Público"
        elif element['attributes']['TipoCE'] == '14':
            level = "Telesecundaria"
        elif element['attributes']['TipoCE'] == '6':
            level = "Colegio Técnico Profesional"
        elif element['attributes']['TipoCE'] == '7':
            level = "Colegio Virtual"
        elif element['attributes']['TipoCE'] == '17':
            level = "CONED"
        elif element['attributes']['TipoCE'] == '3':
            level = "Colegio Nocturno"
        elif element['attributes']['TipoCE'] == '2':
            level = "CINDEA"
        elif element['attributes']['TipoCE'] == '11':
            level = "IPEC"
        elif element['attributes']['TipoCE'] == '15':
            level = "Enseñanza Especial"
        elif element['attributes']['TipoCE'] == '4':
            level = "Colegio Privado"
        elif element['attributes']['TipoCE'] == '1':
            level = "CAIPAD"
        elif element['attributes']['TipoCE'] == '9':
            level = "Escuela Privada"
        elif element['attributes']['TipoCE'] == '19':
            level = "Multiple"
        elif element['attributes']['TipoCE'] == '12':
            level = "Preescolar Privado"
        else:
            level = ""

        school.append(level)
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append(element['attributes']['CODPresupuesto'])
        school.append(element['attributes']['Telefono'])
        school.append("")
        school.append("")
        school.append("") #scale1
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append("")
        school.append(element['attributes']['LONGITUD'])
        school.append(element['attributes']['LATITUD'])
        school_fragment.append(school)
    id_query = last_id
    print('Current id:' + str(last_id))


with open(route+'private_schools.csv', mode='w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'State', 'Municipality', 'Type1', 'Type2', 'Type3', 'Type4', 'Type5', 'Type6', 'Type7', 'Type8', 'Type9', 'Type10',  'Scale1', 'Scale2', 'Scale3', 'Scale4', 'Scale5', 'Scale6', 'Scale7', 'Scale8', 'Scale9', 'Scale10', 'Longitude', 'Latitude'])
    writer.writerows(school_fragment)