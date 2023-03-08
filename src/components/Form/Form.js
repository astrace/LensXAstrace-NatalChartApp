import React, { useEffect, useState } from "react";
import { useWeb3React } from '@web3-react/core';
import TextField from '@mui/material/TextField';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import GoogleMaps from './GeoAutocomplete.tsx';
import CustomDateField from './CustomDateField.js';
import CustomTimeField from './CustomTimeField.js';
import Button from '../Buttons/Button.js';
import styles from './Form.module.css';

export default function Form(props) {
  const { active } = useWeb3React();
  const [value, setValue] = useState('');

  // as soon as wallet is disconnected, go back to "home"
  useEffect(() => {
    if (!active) {props.changePage("home");}
  }, [active])

  return (
    <div className={styles.container}>
      <button onClick={() => props.changePage("home")} className={styles.backButton}>← Go Back</button>
      <h1>Launch your Lens astrological profile </h1>
      <form>
        <GoogleMaps />
        <CustomDateField />
        <CustomTimeField />
      </form>
      <Button text="Mint NFT" />
      <p>Mint price: 0.02 ETH</p>
    </div>
)};
