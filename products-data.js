/* ============================================================
   SourceToGulf 货盘数据 —— 全部来自 ChinaGoods（义乌小商品城官方平台）实搜
   ------------------------------------------------------------
   上新货/改价/下架：只改这个文件，products.html 自动更新。
   ------------------------------------------------------------
   字段说明：
   cat        品类 key（和 CATEGORIES 一致）
   name_en/ar 英文名 / 阿拉伯名
   img        图片路径（/images/products/xxx.jpg）
   fob_cny    ChinaGoods 档口批发价，人民币/件（2026-08 实搜价）
   weight_kg  单件带包装重量 kg（估算值，下单前以实际称重为准）
   moq        最小起订量（估算，可与档口谈）
   lead_days  备货天数
   hot        true = 卡片显示 HOT 角标
   src(注释)  ChinaGoods 商品源链接，用于内部核价溯源
   ------------------------------------------------------------
   到岸价 = fob_cny/7.15 + 菜鸟中东专线运费(MOQ总重)/MOQ
   ⚠️ 图片为平台供应商图，正式上线前建议换成自己 QC 实拍图
   ⚠️ MOQ/重量/货期为估算值，下单前与档口核实
   ============================================================ */

var PRODUCTS_UPDATED = '2026-08';

var CATEGORIES = [
  { key:'home-fragrance', en:'Home fragrance & diffusers', ar:'معطرات المنزل' },
  { key:'seasonal',       en:'Ramadan & Eid seasonal', ar:'مواسم رمضان والعيد' },
  { key:'fashion',        en:'Hijab accessories & jewelry', ar:'إكسسوارات الحجاب والمجوهرات' },
  { key:'tech',           en:'Phone & car accessories', ar:'اكسسوارات الجوال والسيارة' },
  { key:'home',           en:'Home & kitchen', ar:'المنزل والمطبخ' },
  { key:'beauty-toys',    en:'Beauty tools', ar:'أدوات التجميل' }
];

var PRODUCTS = [
  /* ================ home-fragrance（20）================ */
  { cat:'home-fragrance', name_en:'Reed diffuser set — flameless room fragrance', name_ar:'معطر غرفة بالقصبات بلا لهب', img:'/images/products/reed-diffuser.jpg',
    fob_cny:16.00, weight_kg:0.45, moq:24, lead_days:5, hot:true }, // 无火藤条香薰室内酒店家用摆件高级感香氛厕所清新除臭扩香香薰 | 源: https://www.chinagoods.com/store/goodsdetail/2036261522069049346
  { cat:'home-fragrance', name_en:'Wood-tone flameless aroma ornament', name_ar:'معطر منزلي بلا لهب', img:'/images/products/aroma-ornament.jpg',
    fob_cny:13.80, weight_kg:0.3, moq:48, lead_days:5, hot:false }, // 木质香无火香薰摆件高级卧室家用香薰室内卫生间除臭持久清香香氛 | 源: https://www.chinagoods.com/store/goodsdetail/1962340476326699009
  { cat:'home-fragrance', name_en:'Gardenia flameless room fragrance', name_ar:'معطر غرفة برائحة الياسمين', img:'/images/products/hf-01.jpg',
    fob_cny:5.58, weight_kg:0.3, moq:48, lead_days:5, hot:false }, // 香薰香氛栀子花香薰室内无火香氛房间卫生间卧室厕所持久高级感香水 | 源: https://www.chinagoods.com/store/goodsdetail/1836415039717158913
  { cat:'home-fragrance', name_en:'Budget room fragrance set (LF558)', name_ar:'طقم معطر غرفة اقتصادي', img:'/images/products/hf-02.jpg',
    fob_cny:2.10, weight_kg:0.15, moq:100, lead_days:5, hot:false }, // 香薰LF558 | 源: https://www.chinagoods.com/store/goodsdetail/1864578775535763457
  { cat:'home-fragrance', name_en:'Wardrobe scented sachets — anti-moth', name_ar:'أكياس معطرة للخزانة ضد العث', img:'/images/products/hf-03.jpg',
    fob_cny:6.20, weight_kg:0.05, moq:200, lead_days:5, hot:false }, // 衣物淡香水味，衣柜香袋香包除味防霉防虫飘香薰香囊汽车卧室 | 源: https://www.chinagoods.com/store/goodsdetail/2190769
  { cat:'home-fragrance', name_en:'Car fragrance beads & hanging tablets', name_ar:'حبيبات معطرة وحبائل معطرة للسيارة', img:'/images/products/hf-04.jpg',
    fob_cny:12.00, weight_kg:0.12, moq:100, lead_days:5, hot:false }, // 车载香水香珠汽车香薰香片高档车内挂件 | 源: https://www.chinagoods.com/store/goodsdetail/1986702083310059521
  { cat:'home-fragrance', name_en:'Room air-freshener diffuser oil', name_ar:'زيت معطر للغرف والتواليت', img:'/images/products/hf-05.jpg',
    fob_cny:12.50, weight_kg:0.35, moq:48, lead_days:5, hot:false }, // 家用室内香熏 房间空气清新剂香薰厕所除臭持久香薰精油批发 | 源: https://www.chinagoods.com/store/goodsdetail/1694259358218903553
  { cat:'home-fragrance', name_en:'AMBAR imported European reed diffuser', name_ar:'معطر أوروبي مستورد بالقصبات', img:'/images/products/hf-06.jpg',
    fob_cny:76.56, weight_kg:0.9, moq:12, lead_days:7, hot:false }, // 欧洲大牌AMBAR香薰100%原包装进口天然植物原液 | 源: https://www.chinagoods.com/store/goodsdetail/1890216701412220929
  { cat:'home-fragrance', name_en:'Indian sandalwood cone incense + burner', name_ar:'بخور صندل هندي مع مبخرة', img:'/images/products/hf-07.jpg',
    fob_cny:15.00, weight_kg:0.25, moq:48, lead_days:5, hot:false }, // 檀香-疗愈、财富、商业胜利 SANDAL/印度天然锥香【送香炉】 | 源: https://www.chinagoods.com/store/goodsdetail/3438903
  { cat:'home-fragrance', name_en:'Maike Coco soft home fragrance series', name_ar:'سلسلة معطرات منزلية ناعمة', img:'/images/products/hf-08.jpg',
    fob_cny:34.50, weight_kg:0.5, moq:24, lead_days:5, hot:false }, // 迈克可可家居香薰满堂幽香香薰系列细腻柔和 | 源: https://www.chinagoods.com/store/goodsdetail/6202565
  { cat:'home-fragrance', name_en:'500ml China-chic reed diffuser (gift box)', name_ar:'معطر بالقصبات 500 مل بعلبة هدية', img:'/images/products/hf-09.jpg',
    fob_cny:39.00, weight_kg:0.7, moq:24, lead_days:7, hot:true }, // 小红书国潮风无火香薰伴手礼厕所持久散香家用卧室内500ML酒店香熏摆件 | 源: https://www.chinagoods.com/store/goodsdetail/1923749247098249217
  { cat:'home-fragrance', name_en:'Room air-freshener diffuser oil (supplier B)', name_ar:'زيت معطر للغرف (مورد بديل)', img:'/images/products/hf-10.jpg',
    fob_cny:12.50, weight_kg:0.35, moq:48, lead_days:5, hot:false }, // 家用室内香熏 房间空气清新剂香薰厕所除臭持久香薰精油批发 | 源: https://www.chinagoods.com/store/goodsdetail/1991324054058672129
  { cat:'home-fragrance', name_en:'Living-room aroma bottle w/ rattan sticks', name_ar:'زجاجة معطر للصالة بالقصبات', img:'/images/products/hf-11.jpg',
    fob_cny:14.50, weight_kg:0.4, moq:48, lead_days:5, hot:false }, // 香薰精油厕所卫生间香水香氛芳香客厅摆件空气清新剂无火香薰 | 源: https://www.chinagoods.com/store/goodsdetail/1541310443490717698
  { cat:'home-fragrance', name_en:'Flameless bedroom diffuser oil', name_ar:'معطر غرفة نوم بلا لهب', img:'/images/products/hf-12.jpg',
    fob_cny:8.80, weight_kg:0.3, moq:60, lead_days:5, hot:false }, // 无火香薰精油家用卧室内熏香房间摆件香水厕所空气清新剂香薰 | 源: https://www.chinagoods.com/store/goodsdetail/3957177
  { cat:'home-fragrance', name_en:'Solid fragrance balm — car & home', name_ar:'معطر جلدي للسيارة والمنزل', img:'/images/products/hf-13.jpg',
    fob_cny:4.50, weight_kg:0.08, moq:200, lead_days:5, hot:true }, // 2024新款室内香薰固体香膏 梦缘家居香薰膏创意摆件汽车香水摆件 | 源: https://www.chinagoods.com/store/goodsdetail/1835203912287039490
  { cat:'home-fragrance', name_en:'Wardrobe scented wax tablets (gift box)', name_ar:'أقراص شمعية معطرة للخزانة بعلبة هدية', img:'/images/products/hf-14.jpg',
    fob_cny:47.00, weight_kg:0.4, moq:24, lead_days:7, hot:false }, // 衣柜衣橱香薰蜡片妈妈礼物伴手礼礼盒香薰片香氛闺蜜礼品 | 源: https://www.chinagoods.com/store/goodsdetail/1873625670070689793
  { cat:'home-fragrance', name_en:'Car air freshener — flameless oil', name_ar:'معطر هواء للسيارة بالزيت', img:'/images/products/hf-15.jpg',
    fob_cny:7.00, weight_kg:0.15, moq:100, lead_days:5, hot:false }, // 车载空气清新剂无火香薰精油熏香 | 源: https://www.chinagoods.com/store/goodsdetail/1909530715831554049
  { cat:'home-fragrance', name_en:'Tea-scent flameless fragrance liquid', name_ar:'معطر سائل برائحة الشاي', img:'/images/products/hf-16.jpg',
    fob_cny:6.00, weight_kg:0.25, moq:100, lead_days:5, hot:false }, // 新款茶香系无火香薰液熏香卧室内香薰房间客厅留香水香氛除味去味 | 源: https://www.chinagoods.com/store/goodsdetail/1835180106155831297
  { cat:'home-fragrance', name_en:'Dried-flower reed diffuser set', name_ar:'طقم معطر بالقصبات والزهور المجففة', img:'/images/products/hf-17.jpg',
    fob_cny:13.50, weight_kg:0.45, moq:24, lead_days:5, hot:false }, // 无火香薰精油套装 室内香熏干花藤条自然挥发 | 源: https://www.chinagoods.com/store/goodsdetail/4552867
  { cat:'home-fragrance', name_en:'Mini incense sticks box — long-lasting', name_ar:'علبة بخور صغيرة برائحة تدوم', img:'/images/products/hf-18.jpg',
    fob_cny:1.73, weight_kg:0.05, moq:300, lead_days:5, hot:true }, // 小盒raj小方支香薰 线香持久清新 | 源: https://www.chinagoods.com/store/goodsdetail/3405847

  /* ================ seasonal（20）================ */
  { cat:'seasonal', name_en:'Ramadan crescent lantern (laser-cut)', name_ar:'فانوس رمضان بهلال محفور', img:'/images/products/ramadan-lantern.jpg',
    fob_cny:5.30, weight_kg:0.25, moq:100, lead_days:7, hot:true }, // 斋月月亮顶圆顶镭射雕刻风灯提灯蜡烛灯 | 源: https://www.chinagoods.com/store/goodsdetail/1594518133552177153
  { cat:'seasonal', name_en:'Ramadan & Eid atmosphere string lights', name_ar:'أضواء أجواء رمضان والعيد', img:'/images/products/ramadan-lights.jpg',
    fob_cny:7.00, weight_kg:0.15, moq:100, lead_days:7, hot:false }, // 斋月氛围灯开斋节日装饰灯家用LED照明 | 源: https://www.chinagoods.com/store/goodsdetail/2044676349626818562
  { cat:'seasonal', name_en:'Ramadan candle lamp — table centerpiece', name_ar:'مصباح شمعة رمضاني للطاولة', img:'/images/products/sd-01.jpg',
    fob_cny:17.39, weight_kg:0.3, moq:100, lead_days:7, hot:false }, // 跨境新款斋月装饰品蜡烛灯斋月装扮灯场景布置桌面摆件 | 源: https://www.chinagoods.com/store/goodsdetail/1494144877052289025
  { cat:'seasonal', name_en:'Ramadan book lamp / hand-held lantern gift', name_ar:'مصباح كتاب رمضاني هدية', img:'/images/products/sd-02.jpg',
    fob_cny:9.50, weight_kg:0.25, moq:100, lead_days:7, hot:false }, // 新款斋月装饰书灯风灯摆件礼品手提装饰小夜灯 | 源: https://www.chinagoods.com/store/goodsdetail/1692410472107483137
  { cat:'seasonal', name_en:'Ramadan star & moon LED string lights', name_ar:'إضاءة LED نجمة وهلال لرمضان', img:'/images/products/sd-03.jpg',
    fob_cny:2.50, weight_kg:0.08, moq:200, lead_days:7, hot:true }, // 斋月新款led星月灯串满天星彩灯装饰灯房间ins少女心拍照道具 | 源: https://www.chinagoods.com/store/goodsdetail/1688714786524471297
  { cat:'seasonal', name_en:'Moon-and-star curtain lights (LED)', name_ar:'إضاءة ستائر هلال ونجوم', img:'/images/products/sd-04.jpg',
    fob_cny:17.00, weight_kg:0.3, moq:100, lead_days:7, hot:false }, // 厂家直供LED月抱星窗帘灯ins房间装饰灯星月灯串彩灯星星灯批发 | 源: https://www.chinagoods.com/store/goodsdetail/1680144313049341953
  { cat:'seasonal', name_en:'Mini star-moon curtain string lights', name_ar:'إضاءة ستائر صغيرة نجوم وأهلّة', img:'/images/products/sd-05.jpg',
    fob_cny:4.00, weight_kg:0.1, moq:200, lead_days:7, hot:false }, // led星月窗帘灯小彩灯闪灯串灯满天星房间卧室布置网红装饰星星灯 | 源: https://www.chinagoods.com/store/goodsdetail/18603
  { cat:'seasonal', name_en:'Waterproof icicle curtain lights', name_ar:'إضاءة ستائر مقاومة للماء', img:'/images/products/sd-06.jpg',
    fob_cny:11.80, weight_kg:0.25, moq:100, lead_days:7, hot:false }, // LED星月窗帘灯星星灯节日房间客厅布置装饰灯户外防水冰条灯串灯 | 源: https://www.chinagoods.com/store/goodsdetail/1965327588440768514
  { cat:'seasonal', name_en:'Dual-color star & moon light (24 LEDs)', name_ar:'إضاءة نجمة وهلال بلونين', img:'/images/products/sd-07.jpg',
    fob_cny:20.00, weight_kg:0.2, moq:100, lead_days:7, hot:false }, // -24双色星月灯 | 源: https://www.chinagoods.com/store/goodsdetail/2018456
  { cat:'seasonal', name_en:'20-LED star & moon decorative lights', name_ar:'إضاءة زينة 20 لمبة نجوم وأهلّة', img:'/images/products/sd-08.jpg',
    fob_cny:6.00, weight_kg:0.1, moq:200, lead_days:7, hot:false }, // 20头星月led装饰灯 | 源: https://www.chinagoods.com/store/goodsdetail/2881714
  { cat:'seasonal', name_en:'Star & moon lantern light', name_ar:'فانوس نجمة وهلال', img:'/images/products/sd-09.jpg',
    fob_cny:8.00, weight_kg:0.12, moq:200, lead_days:7, hot:false }, // 星月灯 | 源: https://www.chinagoods.com/store/goodsdetail/3551539
  { cat:'seasonal', name_en:'Mini star & moon light', name_ar:'إضاءة صغيرة نجمة وهلال', img:'/images/products/sd-10.jpg',
    fob_cny:3.00, weight_kg:0.08, moq:300, lead_days:7, hot:false }, // 星月灯 | 源: https://www.chinagoods.com/store/goodsdetail/3141592
  { cat:'seasonal', name_en:'Solar curtain lights — outdoor / camping', name_ar:'إضاءة ستائر شمسية للتخييم', img:'/images/products/sd-11.jpg',
    fob_cny:17.99, weight_kg:0.3, moq:100, lead_days:7, hot:false }, // led星月窗帘灯太阳能户外防水网红露营星星灯房间布置氛围装饰灯 | 源: https://www.chinagoods.com/store/goodsdetail/2043537177344233474
  { cat:'seasonal', name_en:'Warm star & moon string lights', name_ar:'إضاءة دافئة نجوم وأهلّة', img:'/images/products/sd-12.jpg',
    fob_cny:20.00, weight_kg:0.2, moq:100, lead_days:7, hot:false }, // 星星月亮造型装饰串灯 梦幻暖光室内氛围灯 | 源: https://www.chinagoods.com/store/goodsdetail/2059110811042201602
  { cat:'seasonal', name_en:'Muslim prayer beads — 33 pcs', name_ar:'مسبحة مسلمة 33 حبة', img:'/images/products/sd-13.jpg',
    fob_cny:1.00, weight_kg:0.03, moq:300, lead_days:5, hot:true }, // 穆斯林念珠，33颗念珠斋月礼品 | 源: https://www.chinagoods.com/store/goodsdetail/1836583621945507842
  { cat:'seasonal', name_en:'Muslim acrylic light sign (gift)', name_ar:'لافتة إضاءة أكريليك هدية', img:'/images/products/sd-14.jpg',
    fob_cny:33.00, weight_kg:0.4, moq:50, lead_days:7, hot:false }, // 穆斯林灯彩灯礼品亚克力灯牌 | 源: https://www.chinagoods.com/store/goodsdetail/1965992548940472321
  { cat:'seasonal', name_en:'Ramadan Muslim wall art (hanging)', name_ar:'لوحة حائط رمضانية معلقة', img:'/images/products/sd-15.jpg',
    fob_cny:2.00, weight_kg:0.1, moq:200, lead_days:5, hot:false }, // 斋月礼品穆斯林挂画 | 源: https://www.chinagoods.com/store/goodsdetail/1588058446957408257
  { cat:'seasonal', name_en:'RAMADAN wooden moon ornament', name_ar:'زينة خشبية على شكل هلال رمضان', img:'/images/products/sd-16.jpg',
    fob_cny:17.80, weight_kg:0.35, moq:100, lead_days:7, hot:true }, // RAMADAN穆斯林工艺品装饰 月亮摆件木质礼品图案定制 | 源: https://www.chinagoods.com/store/goodsdetail/1541227433325965314
  { cat:'seasonal', name_en:'Gold alloy rhinestone incense burner', name_ar:'مبخرة ذهبية مرصعة بالحجر', img:'/images/products/sd-17.jpg',
    fob_cny:30.00, weight_kg:0.5, moq:50, lead_days:7, hot:false }, // 穆斯林斋月 金色合金带钻香炉 炭炉 礼品工艺品 | 源: https://www.chinagoods.com/store/goodsdetail/1588439431256539138
  { cat:'seasonal', name_en:'Rhinestone brooch — gift accessory', name_ar:'دبوس مرصع هدية إسلامية', img:'/images/products/sd-18.jpg',
    fob_cny:5.00, weight_kg:0.03, moq:200, lead_days:5, hot:false }, // 银色镶钻企鹅胸针金属徽章定制时尚胸饰穆斯林款配饰礼品 | 源: https://www.chinagoods.com/store/goodsdetail/2085904257170513921

  /* ================ fashion（20）================ */
  { cat:'fashion', name_en:'Hijab pin set — 20 pcs, camellia design', name_ar:'طقم دبابيس حجاب 20 قطعة', img:'/images/products/hijab-pins-20.jpg',
    fob_cny:7.20, weight_kg:0.06, moq:200, lead_days:5, hot:true }, // 跨境爆款穆斯林纱巾20PCS 纱巾固定针山茶花经典三色头巾固定针 | 源: https://www.chinagoods.com/store/goodsdetail/1999123555653160962
  { cat:'fashion', name_en:'Crystal pear-shaped hijab pin', name_ar:'دبوس حجاب كريستالي', img:'/images/products/hijab-pin-crystal.jpg',
    fob_cny:3.50, weight_kg:0.03, moq:300, lead_days:5, hot:false }, // 穆斯林女纱巾针饰品简约优雅钻针梨形针时尚固定纱巾异域别针 | 源: https://www.chinagoods.com/store/goodsdetail/1963131894542286849
  { cat:'fashion', name_en:'Printed silk-feel square scarf', name_ar:'وشاح مربع مطبع كالحرير', img:'/images/products/fs-01.jpg',
    fob_cny:5.50, weight_kg:0.1, moq:100, lead_days:5, hot:false }, // 简约线条印花丝巾春夏外贸围巾仿真丝方形纱巾百搭领巾 | 源: https://www.chinagoods.com/store/goodsdetail/1545359854806319106
  { cat:'fashion', name_en:'Crystal pear hijab pin (supplier B)', name_ar:'دبوس حجاب كريستالي (مورد بديل)', img:'/images/products/fs-02.jpg',
    fob_cny:7.50, weight_kg:0.03, moq:300, lead_days:5, hot:false }, // 工厂现货 女纱巾针饰品 简约优雅钻针梨形针时尚固定纱巾别针 | 源: https://www.chinagoods.com/store/goodsdetail/6385970
  { cat:'fashion', name_en:'Cotton-linen sun scarf / beach shawl', name_ar:'وشاح قطني كتاني واقٍ من الشمس', img:'/images/products/fs-03.jpg',
    fob_cny:15.00, weight_kg:0.15, moq:100, lead_days:7, hot:false }, // 柳岸围巾夏季新品棉麻纱巾时尚丝巾女披肩防晒纱巾脏染印花沙滩巾 | 源: https://www.chinagoods.com/store/goodsdetail/1574639649217159169
  { cat:'fashion', name_en:'Gradient leopard chiffon shawl', name_ar:'شال شيفون متدرج بنقشة النمر', img:'/images/products/fs-04.jpg',
    fob_cny:15.00, weight_kg:0.13, moq:100, lead_days:7, hot:false }, // 柳岸围巾夏季新品薄款纱巾时尚丝巾女披肩防晒纱巾渐变豹纹沙滩巾 | 源: https://www.chinagoods.com/store/goodsdetail/1574639741231906817
  { cat:'fashion', name_en:'Muslim hooded hijab cap — ethnic style', name_ar:'خمار محجب بطراز تقليدي', img:'/images/products/fs-05.jpg',
    fob_cny:13.00, weight_kg:0.1, moq:100, lead_days:7, hot:false }, // 春夏新款穆斯头巾民族风纱巾帽纱巾套头时尚羽毛帽盖头帽遮发帽 | 源: https://www.chinagoods.com/store/goodsdetail/1692344691522904066
  { cat:'fashion', name_en:'Floral spring neck scarf', name_ar:'وشاح رقبة مزهر للربيع', img:'/images/products/fs-06.jpg',
    fob_cny:9.00, weight_kg:0.08, moq:100, lead_days:5, hot:false }, // 春季新款小碎花纱巾甜美气质少女发带装饰领巾围脖氛围感薄款飘带 | 源: https://www.chinagoods.com/store/goodsdetail/2035261899065798657
  { cat:'fashion', name_en:'Long solid-color Muslim chiffon hijab', name_ar:'حجاب شيفون طويل بلون واحد', img:'/images/products/fs-07.jpg',
    fob_cny:5.00, weight_kg:0.1, moq:100, lead_days:5, hot:true }, // 春秋新款长款丝巾穆斯林纱巾单色围巾披肩压皱 | 源: https://www.chinagoods.com/store/goodsdetail/2014239889403617282
  { cat:'fashion', name_en:'Premium summer scarf / beach shawl', name_ar:'وشاح صيفي فاخر للشاطئ', img:'/images/products/fs-08.jpg',
    fob_cny:58.00, weight_kg:0.15, moq:50, lead_days:7, hot:false }, // 围巾女夏季薄款纱巾韩国东大门百搭丝巾披肩出游沙滩巾防晒纱巾 | 源: https://www.chinagoods.com/store/goodsdetail/2212760
  { cat:'fashion', name_en:'Arabic hijab w/ visor & star-moon chain', name_ar:'حجاب عربي بحاشية وسلسلة نجمة وهلال', img:'/images/products/fs-09.jpg',
    fob_cny:19.00, weight_kg:0.15, moq:50, lead_days:7, hot:true }, // 妮哈纱巾工厂直营 穆斯林头巾 阿拉伯纱巾民族宗教头巾 回族头巾 回族盖头 硬帽檐星月链条款头巾 | 源: https://www.chinagoods.com/store/goodsdetail/2031982205422055425
  { cat:'fashion', name_en:'Malaysian rhinestone pearl chiffon hijab', name_ar:'حجاب شيفون ماليزي مرصع باللؤلؤ', img:'/images/products/fs-10.jpg',
    fob_cny:30.00, weight_kg:0.18, moq:50, lead_days:7, hot:false }, // 穆斯林围巾盖头纱巾马来西亚烫钻烤瓷头巾珍珠雪纺材质高档包丝巾 | 源: https://www.chinagoods.com/store/goodsdetail/1650908
  { cat:'fashion', name_en:'Satin knit shawl — green tones', name_ar:'شال ساتان محبوك بألوان خضراء', img:'/images/products/fs-11.jpg',
    fob_cny:6.00, weight_kg:0.12, moq:100, lead_days:5, hot:false }, // 新丝缎缎面绿色系针织披肩围巾纱巾丝巾 | 源: https://www.chinagoods.com/store/goodsdetail/2072136573328719874
  { cat:'fashion', name_en:'Jamaica-print breathable chiffon shawl', name_ar:'شال شيفون بنقشة جامايكا', img:'/images/products/fs-12.jpg',
    fob_cny:11.00, weight_kg:0.1, moq:100, lead_days:5, hot:false }, // 牙卖加图案雪纺薄款披肩透气纱巾柔透气 | 源: https://www.chinagoods.com/store/goodsdetail/2039234094099681281
  { cat:'fashion', name_en:'Herringbone knit sun scarf', name_ar:'وشاح محبوك مضلع واقٍ من الشمس', img:'/images/products/fs-13.jpg',
    fob_cny:18.00, weight_kg:0.15, moq:100, lead_days:7, hot:false }, // 人字纹汗布毛线纱巾围巾防晒丝巾服装配饰 | 源: https://www.chinagoods.com/store/goodsdetail/2042862119948931073
  { cat:'fashion', name_en:'Lace triangle scarf / hairband (Korean style)', name_ar:'وشاح مثلث دانتيل كوري الطراز', img:'/images/products/fs-14.jpg',
    fob_cny:46.00, weight_kg:0.12, moq:50, lead_days:7, hot:false }, // 轻纱发带气质蕾丝丝巾韩国百搭三角巾小领巾薄款腰带纱巾 | 源: https://www.chinagoods.com/store/goodsdetail/5870207
  { cat:'fashion', name_en:'Hijab magnetic clasps — PVC (1000 pcs)', name_ar:'مشابك مغناطيسية للحجاب PVC', img:'/images/products/fs-15.jpg',
    fob_cny:0.50, weight_kg:0.01, moq:1000, lead_days:5, hot:false }, // 厂家直销 磁钢 磁铁 服装辅料 PVC磁铁扣 磁扣 | 源: https://www.chinagoods.com/store/goodsdetail/883217
  { cat:'fashion', name_en:'Adjustable metal magnetic clasps', name_ar:'مشابك معدنية مغناطيسية قابلة للتعديل', img:'/images/products/fs-16.jpg',
    fob_cny:0.30, weight_kg:0.01, moq:1000, lead_days:5, hot:true }, // 金属磁扣强力吸附可调节磁性扣件通用型 | 源: https://www.chinagoods.com/store/goodsdetail/2071221159200272386
  { cat:'fashion', name_en:'Strong magnetic snap buttons', name_ar:'أزرار مغناطيسية قوية', img:'/images/products/fs-17.jpg',
    fob_cny:1.00, weight_kg:0.01, moq:1000, lead_days:5, hot:false }, // 【超事成】厂家直销 金属磁扣 磁力扣 箱包扣 | 源: https://www.chinagoods.com/store/goodsdetail/1598198919065026562
  { cat:'fashion', name_en:'Magnetic hidden buttons — bags & apparel', name_ar:'مشابك مغناطيسية خفية للحقائب والملابس', img:'/images/products/fs-18.jpg',
    fob_cny:1.00, weight_kg:0.01, moq:1000, lead_days:5, hot:false }, // 磁扣磁铁扣衣服内兜暗扣箱包扣强力吸铁石 | 源: https://www.chinagoods.com/store/goodsdetail/3641737

  /* ================ tech（20）================ */
  { cat:'tech', name_en:'Magnetic aluminium car phone mount', name_ar:'حامل جوال مغناطيسي للسيارة', img:'/images/products/magnetic-mount.jpg',
    fob_cny:1.21, weight_kg:0.09, moq:200, lead_days:5, hot:true }, // 新款车载手机支架 车载支架 铝合金磁性创意汽车懒人支架出风口 | 源: https://www.chinagoods.com/store/goodsdetail/2034844375073738753
  { cat:'tech', name_en:'Suction-cup extendable phone holder', name_ar:'حامل جوال بكوب شفط قابل للتمديد', img:'/images/products/suction-mount.jpg',
    fob_cny:4.00, weight_kg:0.15, moq:100, lead_days:5, hot:false }, // 专属车载手机支架吸盘式汽车手机架长杆伸缩手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/1660568258338455554
  { cat:'tech', name_en:'Telescopic car phone mount', name_ar:'حامل جوال للسيارة قابل للسحب', img:'/images/products/tc-01.jpg',
    fob_cny:8.00, weight_kg:0.2, moq:100, lead_days:5, hot:false }, // 车载手机支架，伸缩手支架机 | 源: https://www.chinagoods.com/store/goodsdetail/3695300
  { cat:'tech', name_en:'Dashboard car phone stand', name_ar:'حامل جوال للوحة القيادة', img:'/images/products/tc-02.jpg',
    fob_cny:22.00, weight_kg:0.3, moq:100, lead_days:5, hot:false }, // 手机支架 车载支架 仪表台支架 车载手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/1497041590461706242
  { cat:'tech', name_en:'CH06 suction windshield extendable mount', name_ar:'حامل شفاط للزجاج الأمامي قابل للتمديد', img:'/images/products/tc-03.jpg',
    fob_cny:13.00, weight_kg:0.25, moq:100, lead_days:5, hot:false }, // CH06汽车吸盘手机支架中控台升级伸缩挡风玻璃车载手机支架懒人 | 源: https://www.chinagoods.com/store/goodsdetail/1540987969874644994
  { cat:'tech', name_en:'Vent mount + cup holder 2-in-1', name_ar:'حامل فتحة تكييف وحامل كوب ثنائي', img:'/images/products/tc-04.jpg',
    fob_cny:11.00, weight_kg:0.2, moq:100, lead_days:5, hot:true }, // 出风口车载手机架水杯架二合一汽车用品 | 源: https://www.chinagoods.com/store/goodsdetail/844294
  { cat:'tech', name_en:'Budget vent-clip phone mount', name_ar:'حامل جوال اقتصادي لفتحة التكييف', img:'/images/products/tc-05.jpg',
    fob_cny:1.00, weight_kg:0.06, moq:300, lead_days:5, hot:true }, // 厂家直销车载手机支架通风口处车载支架手机支架批发两元货源 | 源: https://www.chinagoods.com/store/goodsdetail/1543822048470978562
  { cat:'tech', name_en:'Gravity dashboard mount — rotating', name_ar:'حامل جاذبية دوّار للوحة القيادة', img:'/images/products/tc-06.jpg',
    fob_cny:13.20, weight_kg:0.25, moq:100, lead_days:5, hot:false }, // 车载手机支架汽车仪表盘重力导航车载支架旋转吸盘手机充电支撑架 | 源: https://www.chinagoods.com/store/goodsdetail/2006941476409671681
  { cat:'tech', name_en:'Premium interior car phone mount', name_ar:'حامل جوال فاخر للسيارة', img:'/images/products/tc-07.jpg',
    fob_cny:44.00, weight_kg:0.35, moq:50, lead_days:7, hot:false }, // 车载手机支架汽车用品汽车内饰用品车载手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/2098645
  { cat:'tech', name_en:'Gooseneck suction car mount', name_ar:'حامل عنق مرن بشفاط للسيارة', img:'/images/products/tc-08.jpg',
    fob_cny:8.60, weight_kg:0.3, moq:100, lead_days:5, hot:false }, // 车用手机支架车载专用批发多功能汽车支架软管车载手机支架吸盘 | 源: https://www.chinagoods.com/store/goodsdetail/1976200536459624450
  { cat:'tech', name_en:'Anti-slip universal car mount', name_ar:'حامل سيارة عالمي ضد الانزلاق', img:'/images/products/tc-09.jpg',
    fob_cny:9.10, weight_kg:0.15, moq:100, lead_days:5, hot:false }, // 车载手机支架通用款防滑手机架车载导航支架汽车用品 | 源: https://www.chinagoods.com/store/goodsdetail/2039928155550535682
  { cat:'tech', name_en:'Swivel dashboard / desk lazy mount', name_ar:'حامل دوّار للوحة القيادة والمكتب', img:'/images/products/tc-10.jpg',
    fob_cny:1.00, weight_kg:0.08, moq:300, lead_days:5, hot:false }, // 新款车载手机支架可摆动仪表台导航车载支架桌面懒人万能手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/1532333778894774273
  { cat:'tech', name_en:'Vent gravity suction mount', name_ar:'حامل جاذبية بشفاط لفتحة التكييف', img:'/images/products/tc-11.jpg',
    fob_cny:4.30, weight_kg:0.12, moq:200, lead_days:5, hot:false }, // 汽车导航车用手机支架出风口车载支架吸盘式重力车载手机支架批发 | 源: https://www.chinagoods.com/store/goodsdetail/1516277991364878338
  { cat:'tech', name_en:'K20 telescopic suction mount', name_ar:'حامل شفاط قابل للسحب K20', img:'/images/products/tc-12.jpg',
    fob_cny:8.20, weight_kg:0.22, moq:100, lead_days:5, hot:false }, // K20直销新款汽车导航车载手机支架伸缩吸盘式车载手机支架多功能 | 源: https://www.chinagoods.com/store/goodsdetail/1937341204443906050
  { cat:'tech', name_en:'Universal suction vent mount', name_ar:'حامل شفاط عالمي لفتحة التكييف', img:'/images/products/tc-13.jpg',
    fob_cny:4.50, weight_kg:0.12, moq:200, lead_days:5, hot:false }, // 汽车导航车载手机支架车用吸盘出风口多功能手机架子通用车载手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/4993648
  { cat:'tech', name_en:'RT-60R vent car phone mount', name_ar:'حامل RT-60R لفتحة التكييف', img:'/images/products/tc-14.jpg',
    fob_cny:5.10, weight_kg:0.1, moq:200, lead_days:5, hot:false }, // RT-60R 新款车载手机支架出风口汽车手机支架导航车载支架 | 源: https://www.chinagoods.com/store/goodsdetail/2008013375899742209
  { cat:'tech', name_en:'Auto-lock long-arm lazy mount', name_ar:'حامل ذراع طويلة بقفل تلقائي', img:'/images/products/tc-15.jpg',
    fob_cny:5.50, weight_kg:0.25, moq:100, lead_days:5, hot:false }, // 车载懒人支架自动锁车载手机支架长杆软管车载支架 | 源: https://www.chinagoods.com/store/goodsdetail/912042
  { cat:'tech', name_en:'Multi-function extendable suction stand', name_ar:'حامل شفاط متعدد الوظائف قابل للتمديد', img:'/images/products/tc-16.jpg',
    fob_cny:5.70, weight_kg:0.18, moq:100, lead_days:5, hot:false }, // 车载手机支架吸盘式多功能可伸缩手机架汽车中控台导航支撑架 | 源: https://www.chinagoods.com/store/goodsdetail/1873359376999837698
  { cat:'tech', name_en:'Folding non-slip portable mount', name_ar:'حامل قابل للطي ضد الانزلاق', img:'/images/products/tc-17.jpg',
    fob_cny:30.00, weight_kg:0.25, moq:50, lead_days:7, hot:false }, // 手机支架车载吸盘式防滑便携折叠手机架通用款 | 源: https://www.chinagoods.com/store/goodsdetail/2044674885164695554
  { cat:'tech', name_en:'Desktop lazy folding phone stand', name_ar:'حامل مكتبي قابل للطي والسحب', img:'/images/products/tc-18.jpg',
    fob_cny:2.45, weight_kg:0.15, moq:200, lead_days:5, hot:true }, // 手机桌面支架 可伸缩折叠懒人手机桌面支架 直播刷剧手机支架 | 源: https://www.chinagoods.com/store/goodsdetail/1734751283202260993

  /* ================ home（20）================ */
  { cat:'home', name_en:'Rotary drum vegetable grater & slicer', name_ar:'مقطعة خضار دوارة', img:'/images/products/drum-grater.jpg',
    fob_cny:10.90, weight_kg:0.4, moq:60, lead_days:7, hot:true }, // 旋风滚筒切菜机 多功能切菜器 切丝切片器 手摇擦丝磨粉厨房神器 | 源: https://www.chinagoods.com/store/goodsdetail/1918550983157379074
  { cat:'home', name_en:'Multifunction vegetable slicer (4 blades)', name_ar:'مقطعة خضار متعددة الوظائف', img:'/images/products/veg-slicer.jpg',
    fob_cny:14.00, weight_kg:0.35, moq:60, lead_days:7, hot:false }, // 2021多功能切菜器家用新款切菜器厨房神器厨房必备 | 源: https://www.chinagoods.com/store/goodsdetail/4755330
  { cat:'home', name_en:'Storm chopper — kitchen essentials set', name_ar:'مقطعة سريعة لمستلزمات المطبخ', img:'/images/products/hm-01.jpg',
    fob_cny:22.00, weight_kg:0.5, moq:60, lead_days:7, hot:false }, // 暴风切菜神器生活用品厨房必备好物家庭用品百货厨房神器厨房套装 | 源: https://www.chinagoods.com/store/goodsdetail/1649255869829804033
  { cat:'home', name_en:'Counter-gap storage rack (non-slip)', name_ar:'رف تنظيم لفجوات المطبخ ضد الانزلاق', img:'/images/products/hm-02.jpg',
    fob_cny:31.00, weight_kg:0.6, moq:50, lead_days:7, hot:false }, // 厨房缝隙收纳架收纳厨房神器厨房用品多功能防滑收纳盒 | 源: https://www.chinagoods.com/store/goodsdetail/2042155512243511297
  { cat:'home', name_en:'Mini kitchen gadget — household', name_ar:'أداة مطبخ صغيرة منزلية', img:'/images/products/hm-03.jpg',
    fob_cny:1.00, weight_kg:0.05, moq:300, lead_days:5, hot:false }, // 居家厨房神器小号 创意厨房用品 实用小用具工具 家用懒人必备 | 源: https://www.chinagoods.com/store/goodsdetail/1532293461894160386
  { cat:'home', name_en:'Counter-gap storage rack (compact)', name_ar:'رف تنظيم مضغوط لفجوات المطبخ', img:'/images/products/hm-04.jpg',
    fob_cny:10.50, weight_kg:0.5, moq:60, lead_days:7, hot:false }, // 厨房缝隙收纳架厨房用品收纳神器实用厨房收纳架 | 源: https://www.chinagoods.com/store/goodsdetail/2042494657035051009
  { cat:'home', name_en:'Multi-function gap organizer rack', name_ar:'رف تنظيم متعدد الوظائف', img:'/images/products/hm-05.jpg',
    fob_cny:38.00, weight_kg:0.7, moq:50, lead_days:7, hot:false }, // 厨房缝隙收纳架收纳厨房神器厨房用品多功能防滑厨房用品收纳 | 源: https://www.chinagoods.com/store/goodsdetail/2041892479730540545
  { cat:'home', name_en:'Multi-function chopstick cage', name_ar:'سلة عيدان متعددة الوظائف', img:'/images/products/hm-06.jpg',
    fob_cny:2.50, weight_kg:0.15, moq:200, lead_days:5, hot:false }, // 多功能筷子笼厨房神器神奇厨房装备厨房用品 | 源: https://www.chinagoods.com/store/goodsdetail/3814139
  { cat:'home', name_en:'Viral shredder w/ drain basket', name_ar:'مقطعة مع سلة تصفية', img:'/images/products/hm-07.jpg',
    fob_cny:12.00, weight_kg:0.4, moq:60, lead_days:7, hot:true }, // 抖音爆款多功能切菜神器家用土豆丝切丝器手动厨房神器切菜沥水蓝 | 源: https://www.chinagoods.com/store/goodsdetail/6021265
  { cat:'home', name_en:'Extendable lid & dish rack', name_ar:'رف أغطية وأطباق قابل للتمديد', img:'/images/products/hm-08.jpg',
    fob_cny:12.16, weight_kg:0.5, moq:60, lead_days:7, hot:false }, // 锅盖架厨房神器置物架可伸缩厨具用品收纳架厨房碗盘扩展置物批发 | 源: https://www.chinagoods.com/store/goodsdetail/1897542919365025794
  { cat:'home', name_en:'3-tier hanging storage rack', name_ar:'رف تعليق ثلاثي الطبقات', img:'/images/products/hm-09.jpg',
    fob_cny:23.00, weight_kg:0.7, moq:50, lead_days:7, hot:false }, // 日用百货批发新款收纳挂架收纳厨房神器置物架收纳神器3层 | 源: https://www.chinagoods.com/store/goodsdetail/2042786961103609857
  { cat:'home', name_en:'Drum grater — slice, shred & grind', name_ar:'مقطعة دوارة للتقطيع والبشر والطحن', img:'/images/products/hm-10.jpg',
    fob_cny:25.90, weight_kg:0.45, moq:60, lead_days:7, hot:false }, // 滚筒切菜机多功能切菜神器土豆丝切丝切片器擦丝刨丝磨粉厨房神器 | 源: https://www.chinagoods.com/store/goodsdetail/1999621868307783681
  { cat:'home', name_en:'Dumpling wrapper press mold', name_ar:'قالب عجينة الزلابية', img:'/images/products/hm-11.jpg',
    fob_cny:2.80, weight_kg:0.1, moq:200, lead_days:5, hot:false }, // 家用压皮神器创意包饺子新款厨房神器手动压饺子皮饺子皮模型磨具 | 源: https://www.chinagoods.com/store/goodsdetail/1857286069803077634
  { cat:'home', name_en:'Copper strainer / skimmer — durable', name_ar:'مصفاة نحاسية متينة', img:'/images/products/hm-12.jpg',
    fob_cny:60.00, weight_kg:0.3, moq:50, lead_days:7, hot:false }, // 铜制漏勺不锈钢过滤网厨房神器沥水神器耐用防锈 | 源: https://www.chinagoods.com/store/goodsdetail/2032279123972710401
  { cat:'home', name_en:'Bag sealing clips (multi-use)', name_ar:'مشابك إغلاق الأكياس متعددة الاستخدام', img:'/images/products/hm-13.jpg',
    fob_cny:1.55, weight_kg:0.03, moq:500, lead_days:5, hot:true }, // Z77-301食品袋封口夹多功能厨房神器食品袋封口神器多用封口夹 | 源: https://www.chinagoods.com/store/goodsdetail/1811204910262435842
  { cat:'home', name_en:'4-in-1 grater & slicer (viral)', name_ar:'مبراة ومقطعة رباعية الوظائف', img:'/images/products/hm-14.jpg',
    fob_cny:10.50, weight_kg:0.3, moq:100, lead_days:7, hot:false }, // 抖音爆款刨丝器多功能切菜器四合一厨房神器快速切丝切片 | 源: https://www.chinagoods.com/store/goodsdetail/1561631838772146177
  { cat:'home', name_en:'Mandoline slicer — 6 functions', name_ar:'مقطعة ماندولين بست وظائف', img:'/images/products/hm-15.jpg',
    fob_cny:14.00, weight_kg:0.4, moq:60, lead_days:7, hot:false }, // MANDOLINE SLICER 家用6功能切菜器厨房切菜器 | 源: https://www.chinagoods.com/store/goodsdetail/1052036
  { cat:'home', name_en:'New multifunction chopper (factory direct)', name_ar:'مقطعة متعددة الوظائف جديدة', img:'/images/products/hm-16.jpg',
    fob_cny:32.00, weight_kg:0.6, moq:50, lead_days:7, hot:false }, // 厂家直销新款切菜器，多功能切菜器 | 源: https://www.chinagoods.com/store/goodsdetail/913499
  { cat:'home', name_en:'Vegetable dicer — julienne & cube', name_ar:'مقطعة خضار مكعبات وقشور', img:'/images/products/hm-17.jpg',
    fob_cny:34.73, weight_kg:0.7, moq:50, lead_days:7, hot:false }, // 切菜机多功能切菜器果冻切丁器切丝器刨丝器切菜神器黄瓜切片器 | 源: https://www.chinagoods.com/store/goodsdetail/1595377941391151105
  { cat:'home', name_en:'Stainless potato & garlic shredder', name_ar:'مبراة بطاطس وثوم ستانلس', img:'/images/products/hm-18.jpg',
    fob_cny:18.50, weight_kg:0.4, moq:60, lead_days:7, hot:false }, // 家用土豆切丝器不锈钢多功能切菜器厨房大蒜萝卜切菜切片机擦丝器 | 源: https://www.chinagoods.com/store/goodsdetail/1634798390918492162

  /* ================ beauty-toys（20）================ */
  { cat:'beauty-toys', name_en:'Soft 7-pc makeup brush set', name_ar:'طقم فرش مكياج 7 قطع', img:'/images/products/brush-7pc.jpg',
    fob_cny:5.20, weight_kg:0.12, moq:100, lead_days:5, hot:true }, // 便携防尘美妆刷子化妆刷套刷7件套超柔软全套高档学生平价超软 | 源: https://www.chinagoods.com/store/goodsdetail/1953627115546554370
  { cat:'beauty-toys', name_en:'8-pc makeup brush set (soft, travel)', name_ar:'طقم فرش مكياج 8 قطع', img:'/images/products/brush-5in1.jpg',
    fob_cny:2.20, weight_kg:0.1, moq:200, lead_days:5, hot:false }, // 8支化妆刷套装全套美妆工具眼影散粉刷软毛初学者便携化妆刷整套 | 源: https://www.chinagoods.com/store/goodsdetail/1727973897928642561
  { cat:'beauty-toys', name_en:'XL bulb powder brush (single)', name_ar:'فرشاة بودرة كبيرة الحجم', img:'/images/products/bt-01.jpg',
    fob_cny:10.50, weight_kg:0.05, moq:200, lead_days:5, hot:false }, // 超大号灯泡散粉刷 便携一支装定妆刷不扎脸化妆刷散粉刷 | 源: https://www.chinagoods.com/store/goodsdetail/1641971100701466625
  { cat:'beauty-toys', name_en:'Makeup brush organizer box', name_ar:'علبة تنظيم فرش المكياج', img:'/images/products/bt-02.jpg',
    fob_cny:8.10, weight_kg:0.25, moq:100, lead_days:5, hot:false }, // 跨境热销化妆刷收纳盒防尘桌面分格化妆品眉笔口红刷子眼影收纳盒 | 源: https://www.chinagoods.com/store/goodsdetail/2060224173467217922
  { cat:'beauty-toys', name_en:'Powder & blush brush — black short handle', name_ar:'فرشاة بودرة وأحمر خدود بمقبض قصير', img:'/images/products/bt-03.jpg',
    fob_cny:9.00, weight_kg:0.06, moq:200, lead_days:5, hot:false }, // 正品散粉刷腮红刷化妆刷粉底扫胭脂蜜粉刷彩妆工具黑色短杆 | 源: https://www.chinagoods.com/store/goodsdetail/1631172548952608769
  { cat:'beauty-toys', name_en:'Brush cleaning & drying box', name_ar:'علبة تنظيف وتجفيف الفرش', img:'/images/products/bt-04.jpg',
    fob_cny:7.50, weight_kg:0.2, moq:100, lead_days:5, hot:true }, // 化妆刷清洁收纳盒便携防尘笔刷化妆蛋粉扑清洗过滤神器刷子晾晒架 | 源: https://www.chinagoods.com/store/goodsdetail/2043613034625441794
  { cat:'beauty-toys', name_en:'Flat foundation brush — no streaks', name_ar:'فرشاة كريم أساس مسطحة', img:'/images/products/bt-05.jpg',
    fob_cny:6.30, weight_kg:0.04, moq:200, lead_days:5, hot:false }, // xixi超薄一字化妆师粉底刷扁平头刀锋初学者无痕遮瑕粉底液化妆刷 | 源: https://www.chinagoods.com/store/goodsdetail/2038495018690105346
  { cat:'beauty-toys', name_en:'Silicone brush holder (self-adhesive)', name_ar:'حامل فرش سيليكون لاصق', img:'/images/products/bt-06.jpg',
    fob_cny:8.50, weight_kg:0.15, moq:100, lead_days:5, hot:false }, // VELEKA 创意硅胶刷架 自动吸附硅胶架 硅胶化妆刷收纳架 | 源: https://www.chinagoods.com/store/goodsdetail/916061
  { cat:'beauty-toys', name_en:'12-pc birch wood brush set (rose gold)', name_ar:'طقم فرش 12 قطعة خشب البتولا', img:'/images/products/bt-07.jpg',
    fob_cny:40.00, weight_kg:0.25, moq:50, lead_days:7, hot:false }, // 伊人宝贝黑色金玫瑰化妆套刷纳米纤维12只桦木眼影刷腮红刷 | 源: https://www.chinagoods.com/store/goodsdetail/213874
  { cat:'beauty-toys', name_en:'Dual-head powder & contour brush', name_ar:'فرشاة مزدوجة الرأس للبودرة والكونتور', img:'/images/products/bt-08.jpg',
    fob_cny:10.00, weight_kg:0.06, moq:100, lead_days:5, hot:false }, // 伊人宝贝炫彩双头化妆刷大号散粉修容单支高光腮红刷初学者粉底刷 | 源: https://www.chinagoods.com/store/goodsdetail/2315963
  { cat:'beauty-toys', name_en:'Rotating brush bucket w/ lid', name_ar:'دلو فرش دوّار بغطاء', img:'/images/products/bt-09.jpg',
    fob_cny:7.80, weight_kg:0.3, moq:100, lead_days:5, hot:false }, // 大容量旋转化妆刷桶便携刷子收纳盒筒口红眉笔眼影刷带盖防尘笔筒 | 源: https://www.chinagoods.com/store/goodsdetail/1986353543329185794
  { cat:'beauty-toys', name_en:'Wine-glass shaped powder brush', name_ar:'فرشاة بودرة بشكل كأس', img:'/images/products/bt-10.jpg',
    fob_cny:3.99, weight_kg:0.04, moq:300, lead_days:5, hot:false }, // 高脚杯大号小蛮腰散粉刷化妆刷子单支腮红化妆刷动物毛美妆工具 | 源: https://www.chinagoods.com/store/goodsdetail/1658311842031415297
  { cat:'beauty-toys', name_en:'No-absorb foundation brush (budget)', name_ar:'فرشاة كريم أساس لا تمتص اقتصادية', img:'/images/products/bt-11.jpg',
    fob_cny:1.79, weight_kg:0.03, moq:300, lead_days:5, hot:true }, // 简约个性不吃粉粉底刷创意塑料柄腮红刷批发外出便携尼龙毛化妆刷 | 源: https://www.chinagoods.com/store/goodsdetail/1953627164060749825
  { cat:'beauty-toys', name_en:'12-pc colorful barrel brush set', name_ar:'طقم فرش ملون 12 قطعة بدلو', img:'/images/products/bt-12.jpg',
    fob_cny:7.50, weight_kg:0.3, moq:100, lead_days:5, hot:false }, // 厂家直供新款12支彩色化妆刷桶装创意尼龙毛化妆刷套装腮红散粉刷 | 源: https://www.chinagoods.com/store/goodsdetail/1596387623818268674
  { cat:'beauty-toys', name_en:'Dual-head eye shadow brush', name_ar:'فرشاة ظلال مزدوجة الرأس', img:'/images/products/bt-13.jpg',
    fob_cny:5.20, weight_kg:0.03, moq:200, lead_days:5, hot:false }, // 单支化妆刷小号小马毛双头眼影刷便携一支装眼部初学者晕染刷工具 | 源: https://www.chinagoods.com/store/goodsdetail/3492752
  { cat:'beauty-toys', name_en:'5-pc pro travel brush set', name_ar:'طقم فرش محترف 5 قطعات للسفر', img:'/images/products/bt-14.jpg',
    fob_cny:5.60, weight_kg:0.12, moq:100, lead_days:5, hot:false }, // 瑛秀美化妆套刷 化妆师专用便携款5支套刷散粉刷匀粉刷鼻翼高光刷眼影刷 | 源: https://www.chinagoods.com/store/goodsdetail/1989508890063073281
  { cat:'beauty-toys', name_en:'Rotating brush bucket (compact)', name_ar:'دلو فرش دوّار مضغوط', img:'/images/products/bt-15.jpg',
    fob_cny:7.20, weight_kg:0.3, moq:100, lead_days:5, hot:false }, // 大容量旋转化妆刷桶便携刷子收纳盒筒口红眉笔眼影刷防尘笔筒 | 源: https://www.chinagoods.com/store/goodsdetail/1850060392085811201
  { cat:'beauty-toys', name_en:'Beauty blender sponge w/ box', name_ar:'إسفنجة مكياج مع علبة', img:'/images/products/bt-16.jpg',
    fob_cny:1.40, weight_kg:0.02, moq:500, lead_days:5, hot:true }, // 安妮娜蛋盒美妆蛋柔软服帖立体干湿两用美妆蛋粉扑美妆工具 | 源: https://www.chinagoods.com/store/goodsdetail/1577589885372620801
  { cat:'beauty-toys', name_en:'Soft makeup puff sponge', name_ar:'باف مكياج ناعم', img:'/images/products/bt-17.jpg',
    fob_cny:1.50, weight_kg:0.02, moq:500, lead_days:5, hot:false }, // 卡丁娜粉扑美妆蛋柔软上妆粉扑美妆蛋新品 | 源: https://www.chinagoods.com/store/goodsdetail/2030461430718312449
  { cat:'beauty-toys', name_en:'Mushroom-head puff & sponge set', name_ar:'طقم باف وإسفنجة رأس الفطر', img:'/images/products/bt-18.jpg',
    fob_cny:4.50, weight_kg:0.05, moq:300, lead_days:5, hot:false }, // 蘑菇头粉扑配美妆蛋水滴葫芦彩妆蛋套装斜切粉扑 | 源: https://www.chinagoods.com/store/goodsdetail/1678580681234251778

];
