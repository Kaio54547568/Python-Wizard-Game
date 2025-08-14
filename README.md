# Python Shooting Game Original
### Made by : Kaio

Game download link: https://drive.google.com/file/d/1Zkk_KSYsGBGhUU8_ZlgCVnhlvIxSOfmo/view?usp=sharing

 
### Cách để điều khiển:
- Phím A: di chuyển sang trái
- Phím S: di chuyển sang phải
- Phím W: nhảy
- Phím SPACE: bắn đạn
- Phím Q: ném spell
- Phím ESC: Thoát trò chơi

### Cơ chế trò chơi:
#### Về người chơi:
- Người chơi có 100 máu tối đa, 25 mana cơ bản và tối đa 80 mana
- Mỗi lần đánh thường (bấm SPACE) sẽ tiêu tốn 1 mana và bắn ra 1 viên đạn. Viên đạn gây 25 HP dame
- Mỗi lần dùng spell sẽ tiêu tốn 3 mana và ném 1 quả cầu lửa. Khi quả cầu lửa chạm đất hoặc tường, nó sẽ phát nổ, gây 50 HP dame diện rộng.
- Khi người chơi hết mana, sẽ KHÔNG THỂ TẤN CÔNG.
- Khi máu của người chơi về 0, hoặc người chơi rơi xuống vực, hoặc người chơi rơi vào nước thì người chơi sẽ chết và màn chơi kết thúc
#### Về kẻ địch:
- Có 2 loại kẻ địch chính là TreeTrunk và Peashooter
- Cả 2 kẻ địch đều có 100 HP, và sẽ tấn công nếu kẻ địch trong tầm nhìn
- TreeTrunk sẽ có thể di chuyển và tấn công nếu kẻ địch vào trong tầm đánh
- Peashooter không thể di chuyển, bù lại nó có tầm tấn công xa hơn so với TreeTrunk
#### Về ItemBox:
Có 4 ItemBox chính:
- HealthBox (Đỏ): Hộp máu, khi nhận được, người chơi sẽ hồi lại 40 HP
- ManaBox (Xanh dương): Hộp mana bình thường, khi nhận được, người chơi hồi lại 12 mana
- SpellBox (Vàng): Hộp mana mạnh, khi nhận được, người chơi hồi lại 20 mana
- Coin: Đồng xu, người chơi collect các đồng xu

-------------------------------------------------------------------------------------------------------------------
操作方法:
- Aキー: 左に移動
- Sキー: 右に移動
- Wキー: ジャンプ
- SPACEキー: 弾を撃つ
- Qキー: スペルを投げる
- ESCキー: ゲームを終了する

ゲームメカニクス:

プレイヤーについて:
- プレイヤーは最大100HP、基本25マナ、最大80マナを持つ
- 通常攻撃（SPACEキーを押す）ごとに1マナを消費し、1発の弾を撃つ。弾は25HPのダメージを与える
- スペルを使うと3マナを消費し、1つのファイアボールを投げる。ファイアボールが地面や壁に当たると爆発し、範囲内に50HPのダメージを与える
- プレイヤーがマナ切れになると、攻撃できない
- プレイヤーのHPが0になるか、谷に落ちるか、水に落ちると死亡し、ゲームが終了する

敵について:
- 主な敵は2種類あり、TreeTrunkとPeashooterである
- どちらの敵もHPは100で、視界にプレイヤーが入ると攻撃する
- TreeTrunkは移動可能で、近接範囲にプレイヤーが入ると攻撃する
- Peashooterは移動できないが、TreeTrunkより射程が長い

アイテムボックスについて:
4種類のアイテムボックスがある:

- HealthBox（赤）: HP回復ボックス。取得すると40HP回復する
- ManaBox（青）: 通常マナボックス。取得すると12マナ回復する
- SpellBox（黄）: 強力なマナボックス。取得すると20マナ回復する
- Coin: コイン。プレイヤーが収集できる

  
