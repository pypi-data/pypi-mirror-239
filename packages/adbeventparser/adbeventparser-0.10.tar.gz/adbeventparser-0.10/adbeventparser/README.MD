# Parses the output from 'uiautomator events' in real time and converts it to a list of lists / pandas DataFrame.


## pip install adbeventparser


[![YT](https://i.ytimg.com/vi/KtO5h6XospU/maxresdefault.jpg)](https://www.youtube.com/watch?v=KtO5h6XospU)
[https://www.youtube.com/watch?v=KtO5h6XospU]()

```python
EventRecord class for recording events from an Android device using ADB.

This class provides a way to capture events from an Android device using ADB (Android Debug Bridge).
It can parse and display event data in both standard output and Pandas DataFrame formats.

Args:
	adb_path (str): The path to the ADB executable.
	device_serial (str): The serial number of the target Android device.
	print_output (bool, optional): Whether to print event data to the console. Default is True.
	print_output_pandas (bool, optional): Whether to print event data as Pandas DataFrames. Default is False.
	convert_to_pandas (bool, optional): Whether to convert event data to Pandas DataFrames. Default is False.
	parent1replacement (str, optional): A character used to replace temporarily opening square brackets '[' in event data. Default is "\x80".
	parent2replacement (str, optional): A character used to replace temporarily closing square brackets ']' in event data. Default is "\x81".

Methods:
	start_recording(**kwargs): Starts recording events from the device.

Attributes:
	stop: Stops the event recording if True
	results (list): A list of lists containing parsed event data.
	resultsdf (list): A list of Pandas DataFrames containing parsed event data. (if installed)

Example usage
	from adbeventparser import EventRecord
	sua = EventRecord(
		adb_path=r"C:\Android\android-sdk\platform-tools\adb.exe",
		device_serial="127.0.0.1:5555",
		print_output=True,
		print_output_pandas=False,
		convert_to_pandas=False,
		parent1replacement="\x80",
		parent2replacement="\x81",
	)
	sua.start_recording()
	# to stop
	# sua.stop=True
	# the data as a list of lists
	# sua.results
	# the data as pandas (if installed)
	# sua.resultsdf
```