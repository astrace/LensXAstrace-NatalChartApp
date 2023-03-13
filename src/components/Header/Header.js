import Button from '../Buttons/Button.js';
import ConnectWalletButton from '../Buttons/ConnectWalletButton.js';
import Image from 'next/image';
import React, { useState, useEffect, useRef } from 'react';
import WalletConnection from '../../enums/WalletConnection';
import styles from './Header.module.css'
import { switch2Polygon} from '../../utils/networkConnect.js';
import { useWeb3React } from '@web3-react/core';
import { useWindowWidth } from '@react-hook/window-size'

const POLYGON_CHAIN_ID = 137;

function shortenAddr(addr) {
  return addr.slice(0,6) + "…" + addr.slice(38,42);
}

export default function Header(props) {
  /* We use a different logo in the header when viewport is small */
  const [isMobile, setIsMobile] = useState(false);
  const { active, account, chainId } = useWeb3React();
  const { showButton, setShowButton } = useState(false);

  // see: https://blog.sethcorker.com/question/how-to-solve-referenceerror-next-js-window-is-not-defined/
  useEffect(() => {
    setIsMobile(window.innerWidth <= 599 ? true : false);
  }, []);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 599 ? true : false);
    };
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  function ConnButton() {
    if (props.page == "home") {
      // only show address if connected to Polygon network
      if (active && chainId == 137) {
        return <Button text={shortenAddr(account)} />
      }
    } else {
      // form page
      if (!active) {
        return <Button text="Connect" onClick={props.connect} />
      } else {
        if (chainId == 137) {
          return <Button text={shortenAddr(account)} />
        } else {
          return <Button text="Switch Network" onClick={switch2Polygon(library)} />
        }
      }
    }
  }

  return (
    <header className={styles.header}>
      <div className={styles["header-logo"]}>
        {isMobile? (
          <Image
            src="/logo.svg"
            width={200}
            height={30}
          />
        ) : (
          <Image
            src="/astrace_text.svg"
            width={200}
            height={30}
          />
        )}
      </div>
    <ConnButton />
    </header>
  )
}
