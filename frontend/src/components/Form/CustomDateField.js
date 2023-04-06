import React, { useState } from "react";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { DateField } from '@mui/x-date-pickers/DateField';
import { styled } from '@mui/material/styles';

const CustomDateField = styled(DateField)({
  '& label': {
    color: 'red',
  },
  '& .MuiInput': {
    color: 'red',
  },
  '& label.Mui-focused': {
    color: 'red',
  },
  "& .MuiInputBase-input": {
    color: "white"
  },
  '& .MuiInput-underline': {
    borderBottom: '1px solid red'
  },
  '& .MuiInput-underline.Mui-focused:after': {
    borderBottom: '1px solid red'
  },
  '& .MuiInputBase-root::after': {
    borderBottomColor: 'red',
  },
});

export default function CustomDatePicker(props) {
  const [value, setValue] = useState('');

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <CustomDateField
        value={props.value}
        label="Date of Birth"
        onChange={(newValue) => {
          props.setValue(newValue);
        }}
        variant="standard"
      />
    </LocalizationProvider>
)};
