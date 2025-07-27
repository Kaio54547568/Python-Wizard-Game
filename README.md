# Python Shooting Game Original
### Made by : Kaio
 
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


  
