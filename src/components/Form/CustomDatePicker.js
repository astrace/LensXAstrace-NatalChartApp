import React, { useEffect, useState } from "react";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { CustomTextField } from './CustomTextField.js';
import { renderTextInput } from './renderTextInput.js'

export default function CustomDatePicker(props) {
  const [value, setValue] = useState('');

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <DatePicker
        value={value}
        onChange={(newValue) => {
          setValue(newValue);
        }}
        renderInput={(params) => renderTextInput(params, "Date of Birth")}
        disableOpenPicker
      />
    </LocalizationProvider>
)};
