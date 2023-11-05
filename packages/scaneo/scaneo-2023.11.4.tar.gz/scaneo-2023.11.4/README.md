# ScanEO

ScanEO is a Satellite collaborative annotation tool for Earth Observation.

## Instructions

Install ScanEO

```
pip install scaneo
```

Run the user interface

```
scaneo -d <path_to_data>
```

Open ScanEO in the provided URL ([http://localhost:8000](http://localhost:8000/) by default) to start labeling your data.

You can check the interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs) (or the equivalent URL if you changed the port or host).

You can see other options with 

```
scaneo --help
```

If your data is in a cloud bucket, you can work with it directly by providing the appropriate credentials.

## Annotations

Your annoatations will be stored as `GeoJSON` files with the same name of your images, followed by `_labels.geojson`. For example, if you are labeling `image1.tif`, your annotations will be stored in `image1_labels.geojson`. Additionally, a `labels.json` file will be created containing some metadata about your annotations.

If your data folder contains a valid STAC `catalog.json`, ScanEO will work in STAC mode, using the [label extension](https://github.com/stac-extensions/label). STAC items will be created for each image (if not already present) and the annotations will be stored and linked as separate assets.

## Contact

ScanEO is developed by [Earthpulse](https://earthpulse.ai/). Get in touch with us if you want to know more about ScanEO.