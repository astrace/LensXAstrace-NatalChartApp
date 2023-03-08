
import TextField from '@mui/material/TextField';
import { styled } from '@mui/material/styles';

export const CustomTextField = styled(TextField)({
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

export function renderTextInput(params, label) {
  return (
    <CustomTextField
      {...params}
      label={label}
      variant="standard"
      fullWidth
    />
  )
}

