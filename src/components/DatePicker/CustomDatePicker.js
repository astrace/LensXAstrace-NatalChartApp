import React, { useEffect, useState } from "react";
import TextField from '@mui/material/TextField';
import { DatePicker, LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import styles from './CustomDatePicker.module.css';

export default function CustomDatePicker(props) {
  const [value, setValue] = useState('');

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <div className={styles.datePicker}>
        <DatePicker
          className={styles.datePicker}
          label="Time of Birth"
          value={value}
          onChange={(newValue) => {
            setValue(newValue);
          }}
          InputProps={{
            sx : {
              color: "white",
              fontFamily: "Inter",
              "& .MuiSvgIcon-root": {color: "white"}
            }
          }}
          sx={{
            "& .MuiFormControl-root": {color: "white"}
          }}
          renderInput={(params) => <TextField {...params} />}
        />
      </div>
    </LocalizationProvider>
)};
