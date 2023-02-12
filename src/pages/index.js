import Head from 'next/head'
import Image from 'next/image'
import Header from '../components/Header.js'
import styles from '@/styles/Home.module.css'

//const inter = Inter({ subsets: ['latin'] })

export default function Home() {
  return (
    <>
      <Head>
        <title>Launch LENS astrological profile</title>
        <meta name="description" content="Launch your Lens astrological profile" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <main className={styles.main}>
      {/*
        <Image
          className={styles.backgroundImage}
          src="/background-image.png"
          layout='fill'
          objectPosition='center'
        />
        */}
        <div className={styles.bgWrap}>
          <Image
            src="/background-image.png"
            layout="fill"
            objectFit="cover"
            quality={100}
          />
        </div>
        <Header />
      </main>
    </>
  )
}
