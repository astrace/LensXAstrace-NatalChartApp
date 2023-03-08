import React, { useEffect, useState } from "react";
import dayjs, { Dayjs } from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimeField } from '@mui/x-date-pickers/TimeField';
import { renderTextInput } from './renderTextInput.js'
import { styled } from '@mui/material/styles';

const CssTimeField = styled(TimeField)({
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

export default function CustomTimeField(props) {
  const [value, setValue] = useState('');

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <CssTimeField
        label="Time of Birth"
        inputProps={{
          placeholder: "hellp"
        }}
        onChange={(newValue) => {
          setValue(newValue);
        }}
        variant="standard"
      />
    </LocalizationProvider>
)};
