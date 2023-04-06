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

  const handleChange = function () {
    props.setValue
  }

  return (
    <LocalizationProvider dateAdapter={AdapterDayjs} >
      <CssTimeField
        label="Time of Birth"
        value={props.value}
        onChange={(newValue) => {
          console.log("time of birth changed");
          props.setValue(newValue);
        }}
        onSelectedSectionsChange={(sections) => {
          console.log('SECTIONS');
          console.log(sections);
          console.log(props.value);
          console.log(props.value);
        }}
        onError={() => {
          console.log('error');
        }}
        variant="standard"
      />
    </LocalizationProvider>
)};
