import { useState } from "react";
import Head from 'next/head';
import Image from 'next/image';
import Header from '../components/Header/Header.js';
import Button from '../components/Button/Button.js';
import Modal from '../components/Modal/Modal.js';
import Footer from '../components/Footer/Footer.js';
import styles from '@/styles/Home.module.css';
// logos
import background from '../../public/background-image.png';
import ethereum_icon from '../icons/ethereum.svg';
import wallet_connect_icon from '../icons/wallet_connect.svg';

export default function Home() {
  const [showModal, setShowModal] = useState(false);
  return (
    <>
      <Head>
        <title>Launch LENS astrological profile</title>
        <meta name="description" content="Launch your Lens astrological profile" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <div className={styles.bgWrap}>
        <Image
          alt="background"
          src={background}
          placeholder="blur"
          quality={100}
          fill
          sizes="100vw"
          style={{
            objectFit: 'cover',
          }}
        />
      </div>
      <Header />
      <main className={styles.main}>
        <div className={styles["main-text"]}>
          <h1>Launch your Lens astrological profile</h1>
          <p style={{paddingBottom: 10}}>
            Connect your wallet that holds the Lens profile to mint your 
            Soulbound natal chart NFT and retrieve your astro profile.
          </p>
          <Button text="Connect Wallet" onClick={() => setShowModal(true) }/>
          <Modal
            title="Connect Wallet"
            buttons={[
              <Button text="Browser Wallet" src={ethereum_icon} />,
              <Button text="WalletConnect" src={wallet_connect_icon} />
            ]}
            onClose={() => setShowModal(false)}
            show={showModal}
          />
          <p style={{paddingTop: 18}}>
            Don’t have a Lens profile?
            &nbsp;
            <a href="https://www.lens.xyz/" style={{color: 'red', fontWeight: 400}}>See how to get it.</a>
          </p>
        </div>
          <Footer/>
      </main>
    </>
  )
}
