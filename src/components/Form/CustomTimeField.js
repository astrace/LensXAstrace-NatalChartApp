import dayjs, { Dayjs } from 'dayjs';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { TimeField } from '@mui/x-date-pickers/TimeField';
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

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <CssTimeField
        label="Time of Birth"
        value={props.value}
        onChange={(newValue) => {
          props.setValue(newValue);
        }}
        variant="standard"
      />
    </LocalizationProvider>
)};
