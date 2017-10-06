import pandas as pd 
import requests
import numpy as np
import argparse
API_ENDPOINT = "http://api.setlist.fm/rest/0.1/user/{}/attended.json?p={}"


def backup(username, format):
    cols = ['@eventDate', 'artist.@mbid', 'artist.@name','venue.@name',
           'venue.city.@name', 
           'venue.city.country.@code', 'venue.city.country.@name']
           
    rename_cols = ['date','artist_id','artist','venue','city','country_code','country']
    gigs_query = API_ENDPOINT.format(username,1)
    all = (requests.get(gigs_query).json())
    df = pd.io.json.json_normalize(all['setlists']['setlist'])
    gigs = df[cols].values
    
    total = int(all['setlists']['@total'])
    num_pages = int(total/20) + 1
    
    for p in range(2,num_pages+1):
            if 20*p > total:
                print('Processing.. {} out of {}'.format(total, total))
            else:
                print('Processing.. {} out of {}'.format(20*p, total))

            gigs_query = API_ENDPOINT.format(username,p)
            all = (requests.get(gigs_query).json())
            df = pd.io.json.json_normalize(all['setlists']['setlist'])
            if gigs is not None:
                gigs = np.concatenate((gigs,df[cols].values), axis=0)
            else:
                gigs = df[cols].values

    gigs = pd.DataFrame(gigs, columns=rename_cols)
    if format=='excel':
        gigs.to_excel('gigs_{}.xlsx'.format(username), index=None)
    else:
        gigs.to_csv('gigs_{}.csv'.format(username), index=None)

		
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', help='username on setlist.fm', required=True)
    parser.add_argument('-f', '--format', help='format of the output file (csv or excel)', required=False, default='csv')
    args = parser.parse_args()
    print(args)
    
    backup(args.username, format=args.format)