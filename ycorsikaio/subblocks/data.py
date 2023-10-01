from .dtypes import build_dtype, Field

cherenkov_photons_fields = [
    Field(1, "n_photons", dtype="float32"),
    Field(2, "x", unit="cm", dtype="float32"),
    Field(3, "y", unit="cm", dtype="float32"),
    Field(4, "u", dtype="float32"),
    Field(5, "v", dtype="float32"),
    Field(6, "t", unit="ns", dtype="float32"),
    Field(7, "production_height", unit="cm", dtype="float32"),
    Field(8, "wavelength", dtype="float32"),
]




cherenkov_photons_dtype = build_dtype(cherenkov_photons_fields, itemsize=None)



