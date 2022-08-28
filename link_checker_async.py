import asyncio
import aiohttp
import aiofiles
import pandas as pd
import time
headers =   {
   'User-Agent': 'Your User Agent', ###
            }
f = open("output_txt", 'w') ### delete this for blocking overwrite (append only)
xls = pd.ExcelFile("input.xlsx") ###
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
args = [dict_link,keys_link,url_redirected]
args_alternative = [dict_alt,keys_alt,url_redirected_alt]
"""
params: 
i ; index of the current dictionary key.
redirected_url; redirected url or list of redirected urls for the case of broken links that are redirected.
url_dict ; dictionary that includes tag and link information; keys are tags, values are url links.
url_keys ; keys of the dictionary for reaching dictionary values.
alternatives; are the alternative links for the tags, used only if they exists.
### : change the lines according to your configuration when that appears.
"""
class async_link_checker:
    def __init__(self, length):
        self.length = length
    async def __aiter__(self):
        for idx in self.length:
            yield idx
    async def request_sender(session,url_dict,url_keys,redirected_url,i,e):
        #async for i in async_link_checker(list(range(len(dict_link)))):  #async iterable generator function call for the case of async generated loops.
        try:
            async with session.get(url_dict[url_keys[i]],allow_redirects=True,headers=headers) as response:
                response.raise_for_status()
        except(aiohttp.ClientResponseError,
               aiohttp.ClientError,
               aiohttp.http.HttpProcessingError
               ) as errs:
            e += 1
            print('Broken;' + str(errs) + ' tag: ' + url_keys[i] +' link: ' + url_dict[url_keys[i]])
        if str(response.url) == url_redirected: # if str(response.url) in url_redirected: ### if redirected urls are in a list format
            async with aiofiles.open("output.txt", 'a') as f:  ###
                await f.write('broken;' + ' tag: ' + url_keys[i] + ' link: ' + url_dict[url_keys[i]] +'\n')
            print('Broken;' + ' tag: ' + url_keys[i] +' link: ' + url_dict[url_keys[i]] + ' redirected to: ' + str(response.url))
        elif (e == 0): print('Active;' + ' tag: ' + url_keys[i] + ' link: ' + url_dict[url_keys[i]])
        else:
            pass
    async def session_generator(i):
        async with aiohttp.ClientSession() as session:
            await async_link_checker.request_sender(session, *args,i,e=0)
    async def session_generator_alternative(i):
        async with aiohttp.ClientSession() as session:
            await async_link_checker.request_sender(session, *args_alternative,i,e=0)
    async def main():
        await asyncio.gather(*(async_link_checker.session_generator(i) for i in range(len(dict_link))),
                             *(async_link_checker.session_generator_alternative(i) for i in range(len(dict_alt))))
if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(async_link_checker.main())
    end = time.perf_counter()
    print(f'{end-start:.3f}' + ' secs to run')
