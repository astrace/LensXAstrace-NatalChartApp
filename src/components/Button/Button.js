import React from 'react';
import styles from './Button.module.css'

export default function Button(props) {
  return (
    <button onClick={props.onClick} className={styles.button}><div>Connect Wallet</div></button>
  )
}
