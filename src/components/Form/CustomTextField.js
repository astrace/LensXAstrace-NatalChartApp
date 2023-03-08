import TextField from '@mui/material/TextField';
import { styled } from '@mui/material/styles';

export const CustomTextField = styled(TextField)({
  '& label': {
    color: 'red',
  },
  '& .MuiInput-underline': {
    color: 'red',
  },
  '& label.Mui-focused': {
    color: 'red',
  },
  '& .MuiInput-root': {
    '& fieldset': {
      border: 'none',
      borderBottom: '1px solid red',
      borderRadius: 0
    },
    '&:hover fieldset': {
      border: '1px solid red',
    },
    '&.Mui-focused fieldset': {
      borderColor: 'red'
    },
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
