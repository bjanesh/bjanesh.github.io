---
layout: page
title:
---
`wopr> Greetings, Professor Falken.`

`wopr> Would you like to play a game of ODI data processing?`

**Summary** 

`wopr` is a local IU Astro workstation. Its primary use is ODI data processing after the data has been reduced by the [QuickReduce pipeline](https://portal.odi.iu.edu). To account for a balance between processing speed and data volume, `wopr` is equipped with a 500GB solid state drive, a 1 TB spinning drive, 16GB of memory, and a fast workstation processor. We have also written a pipeline to process and stack pODI/5x6ODI data called [odi-tools](https://github.com/bjanesh/odi-tools), which is in use on `wopr`. Documentation for ODI data processing with `odi-tools` can be found [here](http://odi-tools.readthedocs.io).

**General Policies**

1. `wopr` **is a restricted access machine**, meaning you need a user account to use it. Contact Bob Lezotte or Bill Janesh to request an account. 

2. **Time on `wopr` is scheduled on a first-come-first-serve basis.** Don't schedule more time than you need. Full processing of a 9-point dither pattern takes about 3-4 hours per filter. The schedule can be found below or at [https://teamup.com/ks78bf366c93189e18](https://teamup.com/ks78bf366c93189e18).

3. **All disk space on `wopr` will be treated as scratch space.** ODI data processing is extremely space intensive. The SSD is appropriately sized for full processing of ~30 5x6 ODI images. Use your space carefully! If you have not cleared your data by the end of your scheduled time, it will be cleared for you. Take your final data products with you!

4. **Final data products will be stored on the IU Scholarly Data Archive.** The details of this process are still pending.

5. **Need help?** If you have technical issues with `wopr` please report them to Bob Lezotte. Critical issues with `odi-tools` should be reported to Bill Janesh or Owen Boberg. Non-critical issues or feature requests should be submitted as a [Github issue](https://github.com/bjanesh/odi-tools/issues). All other communication should be directed to the `wopr-l` mailing list.

**Getting started**

0. Log in to your account.
1. Create a working folder under `/ssd1` with an appropriate name for your data.
2. Get your QuickReduced data using the Download option on ODI-PPA. You probably want to use the `wget` option. Navigate to your data folder and paste the command.
3. Copy and edit a `config.yaml` file to include the appropriate options for your data.
4. Run the `odi-tools` data processing scripts as needed. 
5. Run the clean-up script. This will *compress & move* your final products to your home folder and ***delete*** all intermediate data. Don't do this until you are satisfied with your final results!
6. Notify an administrator when you are finished processing your data.

<iframe src="https://teamup.com/ks78bf366c93189e18" frameborder="0" width="100%" height="350"></iframe> 
