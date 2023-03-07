import React, { useEffect, useState } from "react";
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { CustomTextField } from './CustomTextField.js';

export default function CustomDatePicker(props) {
  const [value, setValue] = useState('');

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <DatePicker
        disableOpenPicker
        label="Date of Birth"
        value={value}
        onChange={(newValue) => {
          setValue(newValue);
        }}
        InputProps={{
          sx : {
            "& .MuiSvgIcon-root": {color: "red"}
          }
        }}
        sx={{
          "& .MuiFormControl-root": {color: "white"}
        }}
        renderInput={(params) => (
          <CustomTextField
            {...params}
            label="Date of Birth"
            fullWidth
          />
        )}
      />
    </LocalizationProvider>
)};
