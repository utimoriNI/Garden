---
title: "たかが特別な時間の終わり / It's Only the End of Special Time"
source: "https://speakerdeck.com/watany/its-only-the-end-of-special-time?slide=27"
author:
  - "[[watany]]"
published: 2025-12-02
created: 2026-11-19
description: "イベント：Developers Boost 2025 ～U35エンジニアの登竜門～公演タイトル：たかが特別な時間の終わり - コーディングエージェント以後の不確実なキャリアについてhttps://event.shoeisha.jp/devboost/20251206/session/6416"
tags:
image: "https://files.speakerdeck.com/presentations/0439be3bab2d468bb87871cf3d9532bd/slide_26.jpg?37626514"
cover: "https://files.speakerdeck.com/presentations/0439be3bab2d468bb87871cf3d9532bd/slide_26.jpg?37626514"
---

イベント：Developers Boost 2025 ～U35エンジニアの登竜門～  
公演タイトル：たかが特別な時間の終わり - コーディングエージェント以後の不確実なキャリアについて  
[https://event.shoeisha.jp/devboost/20251206/session/6416](https://event.shoeisha.jp/devboost/20251206/session/6416)

## Transcript

103 slides

1. ### エンジニアに許された 特別な時間の終わり たかが
2. ### About Me 渡邉 洋平(watany) • 所属：NTTテクノクロス株式会社 • AWS Ambassadors(2024〜) •
	JAWS-UG東京(AWSコミュニティ) 運営 • 寄稿：CodeZine ◦ https://codezine.jp/article/detail/22245 2
3. ### 本講演の位置づけ - 対象：35歳以下のITエンジニア、 ITエンジニアを⽬指す学⽣ - 私が35歳の頃に作ったスライド と、その9か⽉後の現在 (2025/12/6)を踏まえたトークです 3 ・Developers
	Boost 2025 https://event.shoeisha.jp/devboost/20251206 ・エンジニアに許された特別な時間の終わり https://speakerdeck.com/watany/the-end-of-the-special-time-granted-to-engineers
4. ### 「超訳‧猿の⼿」 4
5. ### 猿の⼿(1/3) イギリスの作家W.W.ジェイコブ ズの書いたこの物語は、ある夫 妻が「どんな願い事も叶える代 わりに必ず代償が伴う」と謂れ のあるミイラ化した猿の⼿を、 友⼈から受け取る場⾯から始ま ります。 画像：ChatGPT(GPT-5)による生成 5
6. ### 猿の⼿(2/3) 夫妻が初めに「200ポンドが欲し い」と願うと、彼らの息⼦が⼯ 場の機械に巻き込まれた知らせ と会社からの保険⾦が届きまし た。⾦額は200ポンドであったの で、願いは実現しました。 画像：ChatGPT(GPT-5)による生成 6
7. ### 猿の⼿(3/3) 悲しみに暮れる妻は、猿の⼿に 「息⼦を⽣き返らせてほしい」 と願います。すると真夜中に家の ドアを叩く⾳が聞こえます。ドア の向こうに居る者は誰で、どの ような姿であるかを確信した 時、「ドアを叩く⾳が⽌むよう に」と最後に願い、ドアの⾳が 消え去りました。
	画像：ChatGPT(GPT-5)による生成 7
8. ### エンジニアにとっての 「猿の⼿」とは？ 8
9. ### Coding Agent 9
10. ### LLM Chat 〇〇〇の機能を実装して 設計書を見せてください ＜添付ファイル＞ ありがとうございます。 <コード> テストの結果動きません。エラーは～ 失礼しました<修正済コード> ありがとう、動くコードです
	10
11. ### Coding Agent 〇〇〇の機能を実装して 設計書を読んでもいいですか？ いいよ これがコードです。書き出していいですか？ いいよ <コマンド>このコマンドでテストしていい？ いいよ テストが通ったよ。完成！
	11
12. ### LLM Chat / Coding Agent、何が違ったか • Coding Agentはテキスト⽣成に留まらず ◦ 実装の依頼に対して「計画&振り返り」
	▪ 利⽤者がしたのは承認‧決断のみ ◦ 実装に必要な「ツール実⾏」 ▪ ファイルのRead/Write、コマンド実⾏… • Coding Agent：コード補完やチャット応対を越え、⾃⽴したSWE として振舞うAI Agent ◦ 副操縦⼠/Copilot → 操縦⼠/Pilot 12
13. ### Cline • VS Code Extension コーディングエージェント(OSS) ◦ ”必要になれば⼈間に聞く” Human-in-the-Loop ◦
	”⼈間に聞かない機能” Auto Approve • 多彩なツールの実⾏ ◦ ファイルの作成‧編集、コマンド実⾏ ◦ ヘッドレスブラウザを⽤いたデバッグ ◦ MCP経由でのPlugin機能 https://github.com/cline/cline/blob/main/assets/icons/icon.png 13
14. ### Cline • VS Code Extension コーディングエージェント(OSS) ◦ ”必要になれば⼈間に聞く” Human-in-the-Loop ◦
	”⼈間に聞かない機能” Auto Approve • 多彩なツールの実⾏ ◦ ファイルの作成‧編集、コマンド実⾏ ◦ ヘッドレスブラウザを⽤いたデバッグ ◦ MCP経由でのPlugin機能 14
15. ### Coding Agent - Auto Approve 〇〇〇の機能を実装して 設計書を読みます これがコードです。書き出します <コマンド>このコマンドでテストします テストが通ったよ。完成！
	いいよ いいよ いいよ 15
16. ### 注)盛り上がりを加味し、初出の時期ではない Coding Agentの例 画像：Gemini(Nano Banana Pro)による生成 16
17. ### 何に賭けるか？ • どの製品に賭けてもいいし、賭けなくてもいい • Clineを触って「星取表を待つ時間はない」と私は判断した • 特定のツールに賭けるかは、実は本質ではない 17
18. ### 何に賭けるか？ • どの製品に賭けてもいいし、賭けなくてもいい • Clineを触って「星取表を待つ時間はない」と私は判断した • 特定のツールに賭けるかは、実は本質ではない 18
19. ### ”賭け”の本質 CLINEに全部賭けろ https://zenn.dev/mizchi/articles/all-in-on-cline 19
20. ### ドライバー席を譲る？ 20
21. ### ⾃動運転のレベル 自動運転のレベル 0～5までの定義と車種一覧｜レベル 5はいつ実現するのか？ https://staff.persol-xtech.co.jp/hatalabo/mono\_engineer/568.html 21
22. ### コーディングにおける”⾃動運転”のレベル 副操縦士(Copilot) レベル０ AI支援な し レベル1 AI支援 Chat レベル2 AI支援
	補完 ＋Chat 22
23. ### コーディングにおける”⾃動運転”のレベル 副操縦士(Copilot) レベル０ AI支援な し レベル1 AI支援 Chat レベル2 AI支援
	補完 ＋Chat レベル3 Agent 人間が支 援 レベル4 Agent 人間の支 援なし レベル5 実装の完 全自動生 成 操縦士(Pilot) 23
24. ### コーディングにおける”⾃動運転”のレベル 副操縦士(Copilot) レベル０ AI支援な し レベル1 AI支援 Chat レベル2 AI支援
	補完 ＋Chat レベル3 Agent 人間が支 援 レベル4 Agent 人間の支 援なし レベル5 実装の完 全自動生 成 操縦士(Pilot) ドライバー席 助手席 後部座席 エンジニアがドライバー席を譲ることで次 の段階へ進むことができる 24
25. ### ⾃動運転のアナロジー The 5 levels of AI agent autonomy: learning from
	self-driving cars https://speakerdeck.com/layerx/ai-era-management-and-bet-ai 25 AI Agent 時代のソフトウェア開発を支える AWS Cloud Development Kit (CDK) https://speakerdeck.com/konokenj/everything-as-code-cdk
26. ### ⾃動運転のアナロジー AI時代の経営、Bet AI Vision https://speakerdeck.com/layerx/ai-era-management-and-bet-ai 26
27. ### ドライバー席での⼈間による運転 ≒⼈間によるソフトウェアの実装 ≒エンジニアに許された特別な時間 27
28. ### ドライバー席での⼈間による運転 ≒⼈間によるソフトウェアの実装 ≒エンジニアに許された特別な時間 28
29. ### ドライバー席での⼈間による運転の終わり ≒⼈間によるソフトウェアの実装の終わり ≒エンジニアに許された特別な時間の終わり 29
30. ### エンジニアに許された 特別な時間の終わり 30
31. ### ”私たちの知っているプログラミングの終わり” The End of Programming as We Know It https://www.oreilly.com/radar/the-end-of-programming-as-we-know-it/
	31
32. ### ”私たちの知っているプログラミングの終わり” 32
33. ### 類例：ＡＩマインスイーパ https://x.com/mizloq/status/1897194543503827031 33
34. ### 理詰めだけできる部分を全部AIが、 ⼈間には運試しと結果責任だけが残される 34
35. ### 理詰めだけできる部分を全部AIが、 ⼈間には運試しと結果責任だけが残される 35
36. ### 現状確認(2025-03-14) • ”私たちの知っているプログラミングの終わり” • AIエージェントにドライバー席を譲る未来 • エンジニアには運と責任が残される 36
37. ### 現状確認(2025-03-14→2025-12-06) • ”私たちの知っているプログラミングの終わり” • AIエージェントにドライバー席を譲る未来 • エンジニアには運と責任が残される • 2025年11⽉時点では、エンジニアの主な仕事は「ブ レーキと引き換えに質を⾼める」ものになっているる
	37
38. ### 現状確認(2025-03-14→2025-12-06) • ”私たちの知っているプログラミングの終わり” • AIエージェントにドライバー席を譲る未来 • エンジニアには運と責任が残される • 2025年11⽉時点では、エンジニアの主な仕事は「ブ レーキと引き換えに質を⾼める」ものになっているる
	38
39. ### ブレーキと質
40. ### 質とスピード 和⽥卓⼈⽒(@t\_wada)の代表的な講演シナリオ(2019〜) - 「質と引き換えにスピードを出す」の愚かさ - ”すべきことを省略したスケジュール担保”の損益分岐点は早い - Quick & Dirtyは神話であり、汚いアウトプットを拙速さで誤魔
	化したもの - 何をサボって速度を出してしまっていたか - クオリティ＝内部品質＝保守性を犠牲にした、負債の先送り - ”質速”転化 - コードの品質を保つと開発が速い - コードの品質を保てる「品質の⾼いメンバ」だと開発が速い - コードの品質を保てる「品質の⾼いチーム」だと開発が速い 40
41. ### AI (LLM) Agent PRの件数＝速度が変わらない例 Context Engineering https://blog.langchain.com/context-engineering-for-agents/ 41
42. ### Agent = 定義された⼿段の無いループ What Is An Agent? https://www.aihero.dev/what-is-an-agent 42
43. ### AI Agent ＝ ”tools in a loop” I think “agent”
	may finally have a widely enough agreed upon definition to be useful jargon now https://simonwillison.net/2025/Sep/18/agents/ 43
44. ### AIエージェントを 開発で使うと 速いのか？ 44
45. ### Coding Agentで開発を10倍速にした事例 Classmethod accelerates development velocity with Claude Code https://www.claude.com/customers/classmethod
	How Our Engineering Team Embraced AI and Claude Code for 10x Productivity https://www.treasuredata.com/blog/engineering-team-agentic-ai/ 45
46. ### モノタロウで Cursorを導入してみた理想と現実、それと未来 https://speakerdeck.com/monotaro/monotaroudecursorwodao-ru-sitemitali-xiang-toxian-shi-soretowei-lai?slide=24 PRの件数＝速度が変わらない例 46
47. ### 生成AIによるソフトウェア開発の収束地点 - Hack Fes 2025 https://speakerdeck.com/vaaaaanquish/sheng-cheng-ainiyorusohutoueakai-fa-noshou-shu-di-dian-hack-fes-2025?slide=20 体感速度が向上するも、課題解決速度が低下した例 47
48. ### なぜAIエージェントを 開発で使っても 速くならないのか？ 48
49. ### \- コンテキストエンジニアリング - 仕様駆動開発 - Agentic Review Coding Agent の品質を担保する技術
	49
50. ### Context Engineering =「LLMという関数」の⼊⼒ / 出⼒管理 12-Factor Agents -3. Own your
	context window https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-03-own-your-context-window.md 50
51. ### コンテキストを書く / 選ぶ / 縮める / 分ける ための技術 Context Engineering
	https://blog.langchain.com/context-engineering-for-agents/ 51
52. ### \- コンテキストエンジニアリング - 仕様駆動開発 - Agentic Review Coding Agent の品質を担保する技術
	52
53. ### \> A specification is a kind of (version controlled, human-readable)
	super prompt. — 仕様書とは、一種の（バージョン 管理され、人間が読める）スー パープロンプトです。 仕様駆動開発(Spec-Driven Development) Kiro and the future of AI spec-driven software development https://kiro.dev/blog/kiro-and-the-future-of-software-development/ 53
54. ### \> That’s why we’re rethinking speciﬁcations — not as static
	documents, but as living, executable artifacts that evolve with the project. — 仕様書を静的な⽂書ではなく、 プロジェクトと共に進化する⽣ きた実⾏可能な成果物として捉 え直しています。 仕様駆動開発(Spec-Driven Development) Spec-driven development with AI: Get started with a new open source toolkit https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ 54
55. ### 仕様駆動開発の主なプロセス Cline v3.25: The Coding Agent Built for Hard Problems
	https://cline.bot/blog/cline-v3-25 55
56. ### \- コンテキストエンジニアリング - 仕様駆動開発 - Agentic Review Coding Agent の品質を担保する技術
	56
57. ### ⾒るべき箇所に集中できるとレビューの質が⾼まる “人が見るべきところ”に集中するーイノベーションが語る CodeRabbitの活用法 https://www.coderabbit.ai/ja/blog/how-innovation-uses-coderabbit-ja 57
58. ### エージェント型のレビュー⾃動化 58
59. ### 「Coding Agentの 品質を担保する技術」 とは何だったのか 59
60. ### Vibe Coding =「コーディングレスのプログラミング」 - 狭義Vibe Coding (Andrej Karpathy提唱) - キーボードレス‧⾳声での指⽰、全てを承認
	\- 広義Vibe Coding - Agentに委ねてプロセス(How)に介⼊しない - ⽣成されたコードは読まない - 要求を指⽰し続ければバグはいつか直る Vibe Coding 60
61. ### Vibe Coding is Dead - つまり、「品質を担保する技術」= 反「Vibe Coding」 - ”責任あるコード”のために実施されるVibe
	Codingへのカウン ターカルチャー - 結果として、エンジニアの主な仕事は「スピードを犠牲に質 を⾼める」⽅向へ進もうとしている。 61
62. ### \- 「スピードと引き換えに得た保守性/内部品質」は、 Coding Agentが本来発揮できるスピードより速いのか？ - 「Quick & Dirty」は神話だが「Slow & Quality」に正当性はあるか
	\- ⼈間のQuick = すべきことの省略 - エージェントのQuickは、本当に怠惰さ故なのか - 怠惰を前提とする既存の考え⽅をそのまま当てはめてよいか - 「質とスピード」のテーマに対し、別の⾓度からの検討を試みる 2025年の疑問 62
63. ### \- 「スピードと引き換えに得た保守性/内部品質」は、 Coding Agentが本来発揮できるスピードより速いのか？ - 「Quick & Dirty」は神話だが「Slow & Quality」に正当性はあるか
	\- ⼈間のQuick = すべきことの省略 - エージェントのQuickは、本当に怠惰さ故なのか - 怠惰を前提とする既存の考え⽅をそのまま当てはめてよいか - 「質とスピード」のテーマに対し、別の⾓度からの検討を試みる 2025年の疑問 63
64. ### 質とスピード→
65. ### ド－ピスと質←
66. ### ブレーキと質
67. ### 次の”特別な時間”について • AIエージェントにドライバー席を譲る未来 • エンジニアには運と責任が残される • 2025年11⽉時点では、エンジニアの主な仕事は「ブ レーキと引き換えに質を⾼める」ものになっている 67
68. ### 補助ブレーキ 教習⾞では「危ないな」と思った時に、助⼿席からブレーキを踏む 68 教習車に設置されている補助ブレーキについて https://paperdriver-school.net/hojyo.html
69. ### 助⼿席に座ったが、運転を譲れない - Coding Agentとの開発において「危ないと感じた時の補助ブレー キがエンジニアの役割」という合意が⽣まれつつある - 妥当だが、隙あらば操縦席を奪還するための動きではないか - 注）あくまで現在地でのレビューは必須 -
	「速度と引き換えの品質」が正当化されるのはどのラインか - コーディングを10⽇→1⽇に短縮しても、レビューを9⽇かけ れば相殺される 69
70. ### 合意と壁打ち 対AIのレビューにブレーキはないが、それ⾃体がブレーキになり得る - ⼈間相⼿のレビュー：合意 - レビュアー/レビューイは互いに配慮しつつレビューを進める - レビュアー/レビューイで合意した完成像に現実的な範囲で近 づけられる -
	AI相⼿のレビュー：壁打ち - レビューイの負荷を考慮せずいくらでも追い込める - ⼈間関係(⼝調/表現/衝突/初期化)への「ブレーキ」が不要 - レビュアーの完成像に無制限に近づけられる 70
71. ### IKEA Eﬀect IKEA効果(Norton, Mochon, & Ariely (2012)) →⾃分で労⼒をかけて組み⽴てた製品を、 本来の品質以上に⾼く評価し、愛着を持ち やすい⼼理的傾向
	類例： ‧ホットケーキミックスに卵を⼊れる ‧⾃分でテディベアを組み⽴てる https://www.irasutoya.com/2014/08/blog-post\_488.html 71
72. ### ⾃分で組み⽴てたい - LLMを性悪説で扱うがゆえの、助⼿席からの過剰なブレーキ - 「AI臭いコードを⼊れたくない」 - 時間がかかるのは品質の為か、⼈間らしさのためか - 「重厚なレビューが必須」という前提が愛着に陥らないために 72
73. ### Coding Agentへの無意識のバイアス Coding Agentの登壇‧記事のオチに「結局は技術者が必要」は多い - アンナ‧カレーニナの法則 - 成功に対し失敗の理由は多い＝ナレッジの価値が⾼い - 「結局は⼈間」オチを外すと、AI驚き屋だと評価されてしまう
	\- AI驚き屋：LLMモデル/プロダクトの新機能を過剰に喧伝し、 アテンションを集める⼈ - 「結局は技術者が必要」は、エンジニアが安⼼して”特別な時間” を過ごすためのカーゴカルトではないか 73
74. ### 「ブレーキを踏むのがエンジニアの役割」 「⼈間らしいコードで組み⽴てたい」 「結局は⼈間が必要」 74
75. ### 本当に？ 75
76. ### 補助ブレーキの功罪 https://x.com/erukiti/status/1971771745947508851 76
77. ### チキンレースとブレーキ - ⾃動⾞(Agent)と運転⼿(LLMモデル)の性能は、概ね収束する - CodexとClaude Codeのどちらに賭けても、リリース速度はきっと変わ らないだろう - チキンレースの世界観： -
	崖に向かって⾛り出し、先にブレーキを踏んだ者が「チキン」 - ブレーキを踏まないと命を落とす、早く踏むと勝利から遠のく - エージェントに依存すると破綻するし、疑い続けると勝てない - 事実上、開発速度の⽀配項が「ブレーキング技術」となる 77
78. ### 2026年の⼆重思考 2026年のエンジニアは、⼆つの⽭盾を同時に信じなくてはならない １．エンジニアならAI Agentの出⼒は疑わなくてはいけない ２．性能が⾼まり続けるAI Agentの出⼒を疑ってはいけない 78
79. ### 質とスピード(再掲) 和⽥卓⼈⽒(@t\_wada)の代表的な講演シナリオ(2019〜) - 「質と引き換えにスピードを出す」の愚かさ - ”すべきことを省略したスケジュール担保”の損益分岐点は早い - Quick & Dirtyは神話であり、汚いアウトプットを拙速さで誤
	魔化したもの - 何をサボって速度を出してしまっていたか - クオリティ＝内部品質＝保守性を犠牲にした、負債の先送り - ”質速”転化 - コードの品質を保つと開発が速い - コードの品質を保てる「品質の⾼いメンバ」だと開発が速い - コードの品質を保てる「品質の⾼いチーム」だと開発が速い 79
80. ### ブレーキと質 - 「速さと引き換えに質を⾼める」の神話は永遠か - 妥協無しに速度を出すCoding Agent - そのレビューはクオリティのため？ ”特別な時間”のため？ -
	AIエージェントで確保した時間でのレビュー時間は適切か - エージェントを信頼できているか。 - 負債の解消という名のオーバーエンジニアリングをしていないか - 「ブレーキと質」を⼀致させる能⼒ - ブレーキのタイミングが適切だとコードの品質を保てる - ブレーキのタイミングが適切なメンバだとコードの品質を保てる - ブレーキのタイミングが適切なチームだとコードの品質を保てる 80
81. ### Can you bet? 81
82. ### 🎲 82
83. ### 短期のチャートを追うと不安になる 長期投資と短期投資はどっちがいい？　各メリット・デメリット、銘柄選びのポイントを解説 https://finance.yahoo.co.jp/nisa/article/detail/052 83
84. ### Claude Codeの性能劣化に関する懸念(2025/08-2025/09) A postmortem of three recent issues https://www.anthropic.com/engineering/a-postmortem-of-three-recent-issues 85
85. ### 未来は善くなると⾔われても不安になる 長期投資と短期投資はどっちがいい？　各メリット・デメリット、銘柄選びのポイントを解説 https://finance.yahoo.co.jp/nisa/article/detail/052 86
86. ### IT産業における「機械化⾰命」 現職のSE・PGの人はAIの発達で職がなくなると思っていますか？ https://jp.quora.com/%E7%8F%BE%E8%81%B7%E3%81%AESE-PG%E3%81%AE%E4%BA%BA%E3%81%AFAI%E3%81%AE%E7%99%BA%E9%81%94%E3%81%A7%E8%81%B7%E3%81% 8C%E3%81%AA%E3%81%8F%E3%81%AA%E3%82%8B%E3%81%A8%E6%80%9D%E3%81%A3%E3%81%A6%E3%81%84%E3%81%BE%E3%81%99/answers/1477743830562528 87
87. ### Coding Agentはエンジニア(雇⽤)と競合する AIを生産性向上ではなく賃金抑制のためのツールと考えてみると https://yamdas.hatenablog.com/entry/20251007/ai-is-an-attack-from-above-on-wages 88
88. ### コーディングエージェントを⼿にすると 未来のことを考えてしまう が 未来を考えると今に集中できない 89
89. ### “コーディングが楽になればいいのに” なんて、猿の⼿に願わなければよかった 90
90. ### 本当に？ 91
91. ### 当たり前だったことが当たり前になる Coding Agentとの開発は、既存の考え⽅をそのまま移⾏できる - LLMが扱うファイルはプレーンテキストが好ましい - Unix哲学、Markdown、Everything as Code -
	失敗をAgentへ即時にフィードバック - Type, Test, Format, Lint, Runtime Checks, Pre-commit Hooks, CI(Continuous Integration) - Agentの⾃由度を制御しつつ、⾃⾛⼒を活かす - Git管理、環境分離(DevContainer, WebIDE)、開発者体験 92
92. ### 新しい潮流 - 仕様駆動開発への検証 > Property tests are a great match
	for specification-driven development, — プロパティテスト は、(Kiro が行う ような)仕様駆動開発と非常に相 性が良いです。 Does your code match your spec? https://kiro.dev/blog/property-based-testing/ 93
93. ### 新しい潮流 - エージェントの並列実⾏ ファイル競合を防ぐために、git worktree またはリモートマシンを 使用します。 New Coding Model
	and Agent Interface · Cursor https://cursor.com/ja/changelog/2-0 94
94. ### 新しい潮流 - エージェントの⻑時間駆動 >(前略) 私たちは、⻑時間稼働 するエージェントのためのより 効果的なハーネスを開発するた めに、⼈間のエンジニアにイン スピレーションを求めました。 Effective
	harnesses for long-running agents https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents 95
95. ### Agentic Codingのベストプラクティスは 「エンジニアに許された特別な時間」 の上で成り⽴っている 96
96. ### ”振り⼦と螺旋” 和⽥卓⼈⽒の講演「技術選定の審美眼」で中核的な概念 - 新技術は単純化 - 複雑化の両極を振り⼦のように⾏き来する - 「極端に振れても戻るので、学ばなくていい。」→ No -
	新技術の運動は振り⼦に⾒える。実際の動きは「螺旋状」 - 元には戻らず、最先端へ進む - 核となる強固な部分と、以前との差分 - 最先端の吸収⼒が若⼿の強み / 差分の理解がベテランの強み 97
97. ### 特別な時間は振り⼦のようには返ってこない - 「エンジニアに許された特別な時間」は前の姿とは変わっ て、元には戻らない - 品質と愛着を区別するには今まで積み上げたものが⼤きく、 感情的になってブレーキを強く踏んでしまう - 過去の「エンジニアに許された特別な時間」を嘆いても、振 り⼦のようには戻ってこないだろう
	98
98. ### 螺旋状に進むのならば、今までの全てに意味がある - コーディングエージェントとのエンジニアリングは、先⼈が 積み上げた「技術の螺旋」の上にある - 特別な時間が終わった後の、次の特別な時間は「⼿を動かす こと」で⾒つけられる - 過ぎ去っていく特別な時間より、今と向き合おう。螺旋の先 で「愛着」も「特別な時間」も⾒つけよう
	99
99. ### 完 100
100. ### 元ネタ - たかが特別な時間の終わり 表題               内容 エンジニアに許された特別な時間の終わり https://speakerdeck.com/watany/the-end-of-the-special-time-granted-to-engineers たかが世界の終わり グザヴィエ・ドラン／監督・脚本 https://gaga.ne.jp/sekainoowari-xdolan/
	101
101. ### 元ネタ - エンジニアに許された特別な時間の終わり 表題               内容 CLINEに全部賭けろ https://zenn.dev/mizchi/articles/all-in-on-cline わたしたちに許された特 別な時間の終わり 岡田利規／著
	https://www.shinchosha.co.jp/book/129671/ 102
102. ### 元ネタ - ブレーキと質 表紙‧内容 ※和⽥卓⼈⽒のコーディングエージェントへの ⾒解はこちらが参考になります。 質とスピード（ AWS Dev Day
	2023 Tokyo 特別編、質疑応答用資料付き） https://speakerdeck.com/twada/quality-and-speed-aws-dev-day-2023-tokyo-edition AI時代のソフトウェア開発を考える（ 2025/07版） https://speakerdeck.com/twada/agentic-software-engineering-findy-2025-07-edition 103