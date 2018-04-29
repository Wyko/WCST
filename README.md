# WCST
Wisconsin Card Sorting Test Perseveration Scoring Script

This script contains the logic used to score Heaton's Wisconsin Card Sorting Test. 

This script was designed to score tests in the Inquisit 4 software's .iqdat file format, but it could easily be adapted for any csv-format test results. In its current format, the script expects to find files containing a single test result each (including all the trials for that test in the single file). The files should be arranged in the following directory structure:

    /WCST_Scoring.py
    /TEST_NUM/CLASS_NUM/subject_1_test_results.iqdat
    /TEST_NUM/CLASS_NUM/subject_2_test_results.iqdat
    /TEST_NUM/CLASS_NUM/subject_3_test_results.iqdat
    ...etc

Where test_num is the iteration of tests performed, in case you performed multiple tests on the same class over time, and class_num is the name of a particular group of test subjects. Each individual subject's test results should be in an individual test file in that folder. These details are largely cosmetic, but that's just the way the script works now.

Each test file is arranged in a whitespace-seperated format with one line as a header. The format that the software produces leaves a lot of useless data, so at the top of the script are a few global variables definining the columns wherein we find the appropriate data. If your file contains different columns, this is a simple place to adjust that.

The file format the script expects (Inquisit 4 testing result data) looks like this:

    build	date	time	subject	group	blockcode	blocknum	trialcode	trialnum	stimulusitem1	response	correct	latency
    4.0.10.0	41917	8:52:02	1	1	color	1	color_GreenTriangle1	1	GreenTriangle1.jpg	RedTriangle1	0	5847
    4.0.10.0	41917	8:52:02	1	1	color	1	color_RedCross4	2	RedCross4.jpg	GreenStar2	0	10534
    4.0.10.0	41917	8:52:02	1	1	color	1	color_BlueTriangle2	3	BlueTriangle2.jpg	BlueCircle4	1	4691
    4.0.10.0	41917	8:52:02	1	1	color	1	color_RedCircle1	4	RedCircle1.jpg	RedTriangle1	1	2312
    4.0.10.0	41917	8:52:02	1	1	color	1	color_GreenStar4	5	GreenStar4.jpg	GreenStar2	1	1419

Of these, only the Subject (the test-taker's ID), Blockcode (the currently correct match criteria), Blocknum (Which set number we're on), Stimulusitem1 (The stimulus for each trial), and the Response are relevant. The other columns are ignored.

It is important to note that the script is set up to require the capitalization and formating to be exactly according to this format. The Blockcode must be lowercase "form", "color", or "number". The Stimulus must be ColorShape#.jpg, and the response is ColorShape#.

The result will be a slew of individual analysis files and one summary file per class per test. Subsequent runs of the script will append to the existing files (if any) so be sure to remove the results of previous runs.

Feel free to contact me (wyko.ter.haar+wcst@gmail.com) if you can find some use for the script and I would be happy to help you adjust this for your use case.

If you do use this for your work, feel free to do so. Just please let me know and include my name in your attributions.
