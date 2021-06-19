![](https://live.staticflickr.com/6049/6323682453_f58f16b56b_w_d.jpg "credit to Nick Shillingford")  
Start a python server with the ability to copy your local address to clipboard or send it via email, set a custom port, and/or automatically open in browser of choice.  

**why?** because you're worth it  
[**how?**](#usage)  

### Usage
*Note:* CLI will always defer to execute "root/serve.ext" if the root directory contains a file named "serve.ext"  
*Note:* If/where used, the dot is an optional argument  

 

##### Set preferred browser
```shell
> serve setting -o "path/or/alias/to/your/favourite/browser"
> serve setting --open "path/or/alias/to/your/favourite/browser"
```
*Note:* If unset, the command will open the address with the system default for the chosen protocol  
*Note:* Once set, the command will open the address with this browser by default  

##### Set protocol[^1]
```shell
> serve setting -p "name or prefix of chosen protocol"
> serve setting --protocol "name or prefix of chosen protocol"
```
*Note:* Recognized protocols: http, gopher, gemini  

##### Add script extension[^1][^4]
```shell
> serve setting -s ".ext"
> serve setting --script ".ext"
```
*Note:* Recognized protocols: http, gopher, gemini  

##### Suppress browser [^2]
```shell
> serve running -d
> serve running --dont
```

<!-- ##### Enable blocking
```shell
> serve -b 
> serve --block
```   -->

##### Non-current directory[^5]
```shell
> serve running -r "path/to/project/folder"
> serve running --root "path/to/project/folder"
```  

##### Copy to clipboard[^2]
```shell
> serve running -c
> serve running --copy
```  

##### Send email[^3]
```shell
> serve running -m "email.address@sending.to"
> serve running --mail "email.address@sending.to"
```  
*Note:* Will not work unless a source email has been set in settings. You can use the same flags for setting[^3]  

### Supported Platforms
    - [x] Windows
    - [ ] Linux
    - [ ] Mac
### Supported protocols
    - [ ] Gemini
    - [ ] Gopher
    - [x] HTML
### Supported Email Services
    - [x] Gmail[^6]
    - [ ] Proton
    - [ ] Hotmail
    - [ ] Yahoo
    - [ ] Yandex
### Recognized Scripts
If the targeted directory contains a file named "serve" with any of the following extensions, it will be run automatically  
    - [x] js  
    - [x] py  
    - [x] sh  
    - [x] ps1  
    - [x] bat  



### Notes
[1^]: Will propmt for further info.  
[2^]: Toggles saved value if used as setting.  
[3^]: Accepts argument if used as setting.  
[4^]: Only implemented in setting mode.  
[5^]: Only implemented in running mode.  
[6^]: You must enable 'unsafe' mode (in order to send emails programmatically) manually. 
[6^]:  