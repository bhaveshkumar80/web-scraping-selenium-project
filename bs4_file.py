from bs4 import BeautifulSoup

for page_source in all_page_sources:

    soup = BeautifulSoup(page_source, 'lxml')
        
    try:
        scout_id = soup.select_one('.is24-scoutid__content').get_text(strip=True)
    except:
        scout_id = ""

    try:    
        address = soup.select_one('.zip-region-and-country').get_text(strip=True)
    except:
        address = ""

    try:
        state = soup.select_one('.breadcrumb__item:nth-child(2) .breadcrumb__link').get_text(strip=True)
    except:
        state = ""
        
    try:
        gkeys = []
        gvalues = []
        for i, grid in enumerate(soup.select('.two-fifths , .three-fifths')):
            if i % 2 == 0:
                gkeys.append(grid.get_text(strip=True))
            else:
                gvalues.append(grid.get_text(strip=True))

        grid_dict = {}
        for k, v in zip(gkeys, gvalues):
            grid_dict[k] = v
    except:
        grid_dict = {}
    

    data_dict['Link_Header_Project_Name'] = name
    data_dict['State'] = state
    data_dict['Link_Header_project_Url'] = link_header
    data_dict['Scout id'] = scout_id
    data_dict['Address'] = address
    data_dict['Timestamp'] = datetime.now()
    data_dict['Data'] = grid_dict
               
    All_data_list.append(data_dict)
    with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as f:
        json.dump([], f)

    with open('Kaufen_Anlageobjekte.json', mode='w', encoding='utf-8') as feedsjson:
        json.dump(All_data_list, feedsjson, indent=4, default=str)
