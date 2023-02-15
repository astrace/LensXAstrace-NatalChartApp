import React from 'react';
import styles from './Button.module.css'

export default function Button(props) {
  return (
    <button onClick={props.onClick} className={styles.button}>
      <div>{props.text}</div>
      <div><img src={props.icon}/></div>
    </button>
  )
}
