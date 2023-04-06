import React from 'react';
import Icon from '../Icon/Icon.js';
import styles from './Button.module.css';

export default function Button(props) {
  return (
    <button onClick={props.onClick} className={styles.button}>
      <div className={styles.text}>{props.text}</div>
      {props.src &&
        <div className={styles.icon}><Icon src={props.src} width={25} height={25} /></div>
      }
      </button>
  )
}
