# ValorantAccountManager
v 1.0.0　Release

AccountManager(以下本ツール)は Valorantのアカウントを管理およびランクを追跡するためのアプリケーションです。 
新しいアカウントの登録、ランクの更新、Riot クライアントの起動とアカウントの削除のためのボタンを備えたスクロール可能なリストにアカウントを表示する機能が含まれています。

![3b4f590abf9231fd190c61a2d9f9def8](https://github.com/injectxr/ValorantAccountManager/assets/90289410/bc14f787-6f6c-4222-a805-b29290393baa)

## **注意事項**

	本ツールを使用してのアカウント停止や制限には一切の責任を負いません。	(何も悪いことはしていないけど。。。)
	また本ツールはRiotgames.comから承認されたプログラムではありません。
	本ツールは一切のデータ収集をしていません。
	収益化を目的としたプログラムではありません。



## **設定**　

	RiotClientの場所を設定します
	初期値は(C:\Riot Games\Riot Client\RiotClientServices.exe)に設定されています
	RiotClientが起動してからpyautoguiが起動するまでの待機時間を指定できます
	defaultの値にリセットできます
 
 
アカウント追加

	アカウントを追加します
	必要な情報はID TAGLINE ( # は必要ありません) LoginID Passwordです
 
ランク更新

	ID TAGLINEからValorantAPIを使用して現在表示されているランクと違う場合更新します
	登録されているアカウントが多い場合、本ツールはフリーズする場合がありますが待てば治ります


スクロールページ

CSVに登録されているデータをもとに登録されているアカウントを表示します
  
	起動ボタン
  
		登録されているLoginID PassewordをもとにRiotClientを起動します
		pyautogui を使ってマウスカーソルの移動とID Passの入力をします

	編集ボタン
		編集ウィンドウ
			登録されている情報を編集できるようにしました
		ゴミ箱ボタン
			列を削除します
アカウントソート

		CSVに登録されているアカウントをランク順に並び替えます。



mao 
@injectxr
