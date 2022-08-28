import requests
import pandas as pd
import time

f = open("output.txt", 'w')   ###
xls = pd.ExcelFile("input.xlsx")  ###
df = xls.parse(xls.sheet_names[0])
df = df[['tag','link']]
df = df.reset_index(drop=True)
df_alt = xls.parse(xls.sheet_names[0])
df_alt = df_alt[['tag','alternative_link']]
df_alt = df_alt.reset_index(drop=True)
dict_link = dict(df.values)
keys_link = list(dict_link)
dict_alt = dict(df_alt.values)
keys_alt = list(dict_alt)
url_redirected= 'the url that is redirected when the case of link is broken or expired'  ###
url_redirected_alt= 'the alternative url that is redirected when the case of alternative link is broken or expired' ###
args = [dict_link,keys_link,dict_alt,keys_alt,url_redirected,url_redirected_alt]
"""
params: 
redirected_url; redirected url or list of redirected urls for the case of broken links that are redirected.
url_dict ; dictionary that includes tag and link information; keys are tags, values are url links.
url_keys ; keys of the dictionary for reaching dictionary values.
alternatives; are the alternative links for the tags, used only if they exists.
### : change the lines according to your configuration when that appears.
"""
class sync_link_checker:
    def request_sender(url_dict,url_keys,url_dict_alt,url_keys_alt,redirected_url,redirected_url_alt):
        k = 0
        headers = requests.utils.default_headers()
        headers.update(
            {
                    'User-Agent': 'Your User Agent',   ###
                }
            )
        for i in range(len(url_dict)):
            e = 0
            ea = 0
            print('Checked link count is: ' + str(2*i) if i % 5 == 0 else "")
            try:
                r = requests.get(url_dict[url_keys[i]], allow_redirects = True, headers=headers)
                r.raise_for_status()
            except requests.exceptions.HTTPError as errh:
                print("Http Error: " + str(errh) + ' tag: ' + url_keys[i])
                f.write("Http Error: " + str(errh) + ' tag: ' + url_keys[i] +'\n')
                e += 1
                k += 1
            except requests.exceptions.ConnectionError as errc:
                print("Connection Error: " + str(errc) + ' tag: ' + url_keys[i])
                f.write("Connection Error: " + str(errc) + ' tag: ' + url_keys[i] +'\n')
                e += 1
                k += 1æ
            except requests.exceptions.Timeout as errt:
                print("Timeout Error: " + str(errt) +  ' tag: ' + url_keys[i])
                f.write("Timeout Error: " + str(errt) +  ' tag: ' + url_keys[i] +'\n')
                e += 1
                k += 1
            except requests.exceptions.RequestException as err:
                print("OOps Something Else: " +str(err) + ' tag: ' + url_keys[i])
                f.write("OOps Something Else: " +str(err) + ' tag: ' + url_keys[i] +'\n')
                e += 1
                k += 1
            #except:
            if r.url == redirected_url: # if r.url in redirected_url: ### if redirected urls are in a list format
                f.write('Broken;' + ' tag: ' + url_keys[i] + ' link: ' + url_dict[url_keys[i]] + ' redirected to: ' + str(r.url) + '\n')
                print('Broken;' + ' tag: ' + url_keys[i] + ' link: ' + url_dict[url_keys[i]] + ' redirected to: ' + str(r.url))
                k += 1
            elif (e == 0): print('Active;' + ' tag: ' + url_keys[i] + ' link: ' + url_dict[url_keys[i]])
            else:
                pass
            try:
                r_alt = requests.get(url_dict_alt[url_keys_alt[i]], allow_redirects = True, headers=headers)
                r_alt.raise_for_status()
            except requests.exceptions.HTTPError as err1:
                print("Http Error (alternative): " + str(err1) + ' tag: ' + url_keys_alt[i])
                f.write("Http Error (alternative): " + str(err1) + ' tag: ' + url_keys_alt[i] +'\n')
                ea += 1
                k += 1
            except requests.exceptions.ConnectionError as err2:
                print("Connection Error (alternative): " + str(err2) + ' tag: ' + url_keys_alt[i])
                f.write("Connection Error (alternative): " + str(err2) + ' tag: ' + url_keys_alt[i] +'\n')
                ea += 1
                k += 1
            except requests.exceptions.Timeout as err3:
                print("Timeout Error (alternative): " + str(err3) +  ' tag: ' + url_keys_alt[i])
                f.write("Timeout Error (alternative): " + str(err3) +  ' tag: ' + url_keys_alt[i] +'\n')
                ea += 1
                k += 1
            except requests.exceptions.RequestException as err4:
                print("Other Exception Error (alternative) : " +str(err4) + ' tag: ' + url_keys_alt[i])
                f.write("Other Exception Error (alternative): " +str(err4) + ' tag: ' + url_keys_alt[i] +'\n')
                ea += 1
                k += 1
            #except:
            if r_alt.url == redirected_url_alt: # if r_alt.url in redirected_url_alt: ### if redirected urls are in a list format
                f.write('Broken;' + ' tag: ' + url_keys_alt[i] + ' alternative link: ' + url_dict_alt[url_keys_alt[i]] + ' redirected to: ' + str(r_alt.url) + '\n')
                print('Broken;' + ' tag: ' + url_keys_alt[i] + ' alternative link: ' + url_dict_alt[url_keys_alt[i]] + ' redirected to: ' + str(r_alt.url))
                k += 1
            elif (ea == 0): print('Active;' + ' tag: ' + url_keys_alt[i] + ' alternative link: ' + url_dict_alt[url_keys_alt[i]])
            else:
                pass
        f.close()
        print('Checked link count is: ' + str(2*len(url_dict)))
        print('Broken link count is: ' + str(k))
if __name__ == "__main__":
    start = time.perf_counter()
    sync_link_checker.request_sender(*args)
    end = time.perf_counter()
    print(f'{end-start:.3f}' + ' secs to run')
