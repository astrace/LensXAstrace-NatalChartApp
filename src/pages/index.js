import Head from 'next/head'
import Image from 'next/image'
import Header from '../components/Header.js'
import Footer from '../components/Footer.js'
import styles from '@/styles/Home.module.css'

export default function Home() {
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
          src="/background-image.png"
          layout="fill"
          objectFit="cover"
          quality={100}
        />
      </div>
      <Header />
      <main className={styles.main}>
        <div className={styles["main-text"]}>
          <h1>Launch your Lens astrological profile</h1>
          <p>
            Connect your wallet that holds the Lens profile to mint your 
            Soulbound natal chart NFT and retrieve your astro profile.
          </p>
        </div>
        <div className={styles.footer}>
          <Footer/>
        </div>
      </main>
    </>
  )
}
