import React, { useEffect } from 'react';
import { useWeb3React } from '@web3-react/core';
import { injected } from "../connector.js"
import Icon from '../Icon/Icon.js';
import styles from './Button.module.css';

function shortenAddr(addr) {
  return addr.slice(0,6) + "…" + addr.slice(38,42);
}

export default function ConnectWalletButton(props) {
  const {
    activate,
    deactivate,
    active,
    account
  } = useWeb3React();
 
  async function connect() {
    try {
      await activate(injected)
      localStorage.setItem('isWalletConnected', true)
    } catch (ex) {
      console.log(ex)
    }
  }

  async function disconnect() {
    try {
      deactivate()
      localStorage.setItem('isWalletConnected', false)
    } catch (ex) {
      console.log(ex)
    }
  }

  useEffect(() => {
    const connectWalletOnPageLoad = async () => {
      if (localStorage?.getItem('isWalletConnected') === 'true') {
        try {
          await activate(injected)
          localStorage.setItem('isWalletConnected', true)
        } catch (ex) {
          console.log(ex)
        }
      }
    }
    connectWalletOnPageLoad()
  }, [])

  return (
    <div>
    {!active ? (
      <button onClick={connect} className={styles.button}>
        <div className={styles.text}>Connect Wallet</div>
        {props.src && <div className={styles.icon}><Icon src={props.src} width={25} height={25} /></div>}
      </button>
    ) : (
      <button onClick={disconnect} className={styles.button}>
        <div className={styles.text}>{shortenAddr(account)}</div>
        {props.src && <div className={styles.icon}><Icon src={props.src} width={25} height={25} /></div>}
      </button>
    )}
    </div>
  )
}
