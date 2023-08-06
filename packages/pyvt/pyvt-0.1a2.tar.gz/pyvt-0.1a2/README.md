pyvt
====

Python 3 implementation of the [Virustotal](https://www.virustotal.com/) [Private API](https://www.virustotal.com/en/documentation/private-api/).
In its current form it only implements a subset of the API and is incomplete. 

This module borrows code from, the [virustotal2](https://github.com/Phillipmartin/virustotal2) module.
It uses the same rate limiting logic as virustotal2. Additionally it unifies the output of the API to json format and adds support for bulk queries.


##How To Use

    import pyvt

    api = pyvt.API('~/.virustotal.key')
    # Retrieve list of ips
    api.retrieve(['173.236.179.77', '66.33.221.102'])
    
    # Retrieve list of urls
    api.retrieve(['http://3dtaller.com.ar/',
                  'http://3dtaller.com.ar/wp-content/themes/theme1392/js/jquery.loader.js',
                  'http://3dtaller.com.ar/wp-includes/js/swfobject.js',
                  'http://3dtaller.com.ar/wp-content/themes/theme1392/js/modernizr-2.0.js',
                  'http://3dtaller.com.ar/wp-content/themes/theme1392/js/custom.js',
                  'http://3dtaller.com.ar/wp-content/themes/theme1392/js/jquery-1.6.4.min.js'])
                  
    # Retrieve domain
    api.retrieve('3dtaller.com.ar')
    

##Installiation


    pip3 install pyvt --pre


##Instantiation


    api = pyvt.API('~/.virustotal.key')                                # The default way of using the 
    api = pyvt.API('', api_key=<VT API KEY>, limit_per_min=<number>)   # Providing other parameters

You can pass limit_per_min, which is the number of queries you can perform per minute.  3000 is the default.
You can also alternatively provide your api_key as a string parameter.


API
===

Use the method retrieve() to get an existing report from VirusTotal.  This method's first argument can be:

- a single or list of MD5, SHA1 or SHA256 of files
- a single or list of URLs
- a single or list IP addresses
- a single or list of domain names

retrieve() will attempt to auto-detect what you're giving it.  If you want to be explicit, you can use the thing_type parameter with the values:

- ip
- domain
- hash
- file
- base64
- url

These values are provided as constants that you can use instead in the 'API_Constans' class which you can import as follows
::
    
    from pyvt import API_Constansts


You can use thee scan() method to scan specific URLs. The scan method currently only supports URLs and will through an exception if
anything other than a url is given to it.

###References

[Virustotal Private API](https://www.virustotal.com/en/documentation/private-api/)


