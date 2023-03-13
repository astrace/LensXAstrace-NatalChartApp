import React, { useEffect, useState } from "react";
import { useWeb3React } from '@web3-react/core';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import GoogleMaps from './GeoAutocomplete.tsx';
import CustomDateField from './CustomDateField.js';
import CustomTimeField from './CustomTimeField.js';
import DisabledButton from '../Buttons/DisabledButton.js';
import Button from '../Buttons/Button.js';
import styles from './Form.module.css';

interface MainTextMatchedSubstrings {
  offset: number;
  length: number;
}
interface StructuredFormatting {
  main_text: string;
  secondary_text: string;
  main_text_matched_substrings?: readonly MainTextMatchedSubstrings[];
}
interface PlaceType {
  description: string;
  structured_formatting: StructuredFormatting;
}

export default function Form(props) {
  const { active } = useWeb3React();
 
  const [city, setCity] = React.useState<PlaceType | null>(null);
  const [date, setDate] = React.useState(null);
  const [time, setTime] = React.useState(null);
  const [formFilled, setFormFilled] = React.useState(false);
  
  // as soon as wallet is disconnected, go back to "home"
  useEffect(() => {
    if (!active) {props.changePage("home");}
  }, [active])

  useEffect(() => {
    if (time != null) {
      console.log(time.error);
    } 
    if (city != null && date != null && time != null) {
      setFormFilled(true);
    } else {
      setFormFilled(false);
    }
  }, [city, date, time])

  return (
    <div className={styles.container}>
      <button onClick={() => props.changePage("home")} className={styles.backButton}>← Go Back</button>
      <h1>Launch your Lens astrological profile </h1>
      <form>
        <GoogleMaps value={city} setValue={setCity} />
        <CustomDateField value={date} setValue={setDate} />
        <CustomTimeField value={time} setValue={setTime} />
      </form>
      {formFilled
        ? <Button text="Mint Natal Chart" />
        : <DisabledButton text="Mint Natal Chart" />
      }
      <p>Mint price: 0.02 ETH</p>
    </div>
)};
