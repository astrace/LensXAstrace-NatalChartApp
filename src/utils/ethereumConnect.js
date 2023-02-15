import React, {useState} from 'react'
import {ethers} from 'ethers'

// update account, will cause component re-render
function accountChangedHandler(newAccount, changeAccount) {
	balance = getAccountBalance(newAccount.toString());
	changeAccount(newAccount, balance);
}

function getAccountBalance(account)  {
	window.ethereum.request({method: 'eth_getBalance', params: [account, 'latest']})
	.then(balance => {
		return balance;
	})
	.catch(error => {
		console.log("ERRROR");
		console.log(error.message);
	});
};

export { accountChangedHandler };
