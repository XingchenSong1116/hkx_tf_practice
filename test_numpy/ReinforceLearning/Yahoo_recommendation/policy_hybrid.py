import numpy as np

class HybridLinUCB():
	def __init__(self):
		self.alpha = 2.1 # 1 + np.sqrt(np.log(2/delta)/2)
		self.r1 = 0.8
		self.r0 = -20
		self.d = 6 # dimension of user features = d
		self.k = self.d * self.d # dimension of user-article features = k
		self.article_features = {}
		self.A0 = np.identity(self.k) # A0 : matrix to compute hybrid part, k*k
		self.A0I = np.identity(self.k) # A0I: inverse of A0
		self.b0 = np.zeros((self.k, 1)) # b0 : vector to compute hybrid part, k
		self.Aa = {} # Aa : collection of matrix to compute disjoint part for each article a, d*d
		self.AaI = {} # AaI : collection of matrix to compute disjoint part for each article a, d*d
		self.Ba = {} # Ba : collection of matrix to compute hybrid part, d*k
		self.BaT = {} # BaT : collection of matrix to compute hybrid part, d*k
		self.ba = {} # ba : collection of vectors to compute disjoin part, d*1
		self.AaIba = {}
		self.AaIBa = {}
		self.A0IBaTAaI = {}
		# self.AaIBaA0IBaTAaI = {}
		self.theta = {}
		self.beta = np.zeros((self.k, 1))
		self.article_id_to_index = {}
		self.acticle_max_index = None
		self.z = None
		self.zT = None
		self.xaT = None
		self.xa = None
		print("class name:"+self.__class__.__name__)

	def set_articles(self, article_id_to_embed_map):
		i = 0
		art_len = len(article_id_to_embed_map)
		self.article_features = np.zeros((art_len, 1, self.d))
		self.Aa = np.zeros((art_len, self.d, self.d))
		self.AaI = np.zeros((art_len, self.d, self.d))
		self.Ba = np.zeros((art_len, self.d, self.k))
		self.BaT = np.zeros((art_len, self.k, self.d))
		self.ba = np.zeros((art_len, self.d, 1))
		self.AaIba = np.zeros((art_len, self.d, 1))
		self.AaIBa = np.zeros((art_len, self.d, self.k))
		self.A0IBaTAaI = np.zeros((art_len, self.k, self.d))
		# self.AaIBaA0IBaTAaI = np.zeros((art_len, self.d, self.d))
		self.theta = np.zeros((art_len, self.d, 1))

		# TODO: 在hybrid中，才使用了article的embedding特征
		for key in article_id_to_embed_map:
			self.article_id_to_index[key] = i
			self.article_features[i] = article_id_to_embed_map[key][:]
			self.Aa[i] = np.identity(self.d)
			self.AaI[i] = np.identity(self.d)
			self.Ba[i] = np.zeros((self.d, self.k))
			self.BaT[i] = np.zeros((self.k, self.d))
			self.ba[i] = np.zeros((self.d, 1))
			self.AaIba[i] = np.zeros((self.d, 1))
			self.AaIBa[i] = np.zeros((self.d, self.k))
			self.A0IBaTAaI[i] = np.zeros((self.k, self.d))
			# self.AaIBaA0IBaTAaI[i] = np.zeros((self.d, self.d))
			self.theta[i] = np.zeros((self.d, 1))
			i += 1

	def update(self, reward):
		if reward == -1:
			pass
		elif reward == 1 or reward == 0:
			if reward == 1:
				r = self.r1
			else:
				r = self.r0

			self.A0 += self.BaT[self.acticle_max_index].dot(self.AaIBa[self.acticle_max_index])
			self.b0 += self.BaT[self.acticle_max_index].dot(self.AaIba[self.acticle_max_index])
			self.Aa[self.acticle_max_index] += np.dot(self.xa, self.xaT)
			self.AaI[self.acticle_max_index] = np.linalg.inv(self.Aa[self.acticle_max_index])
			self.Ba[self.acticle_max_index] += np.dot(self.xa, self.zT)
			self.BaT[self.acticle_max_index] = np.transpose(self.Ba[self.acticle_max_index])
			self.ba[self.acticle_max_index] += r * self.xa
			self.AaIba[self.acticle_max_index] = np.dot(self.AaI[self.acticle_max_index], self.ba[self.acticle_max_index])
			self.AaIBa[self.acticle_max_index] = np.dot(self.AaI[self.acticle_max_index], self.Ba[self.acticle_max_index])

			self.A0 += np.dot(self.z, self.zT) - np.dot(self.BaT[self.acticle_max_index], self.AaIBa[self.acticle_max_index])
			self.b0 += r * self.z - np.dot(self.BaT[self.acticle_max_index], self.AaIba[self.acticle_max_index])
			self.A0I = np.linalg.inv(self.A0)
			self.A0IBaTAaI[self.acticle_max_index] = self.A0I.dot(self.BaT[self.acticle_max_index]).dot(self.AaI[self.acticle_max_index])
			# self.AaIBaA0IBaTAaI[self.a_max] = np.matmul(self.AaIBa[self.a_max], self.A0IBaTAaI[self.a_max])
			self.beta = np.dot(self.A0I, self.b0)
			self.theta = self.AaIba - np.dot(self.AaIBa, self.beta)

		else:
			pass


	def recommend(self, timestamp, user_features, candidate_articles):
		article_len = len(candidate_articles) # 20

		# TODO: 此处与disjoint一样,使用了user_feature
		self.xa = np.array(user_features).reshape((self.d,1)) # (6,1)
		self.xaT = np.transpose(self.xa) # (1,6)

		candidate_article_indexs = [self.article_id_to_index[article] for article in candidate_articles]
		# 这些embedding 特征是通过bilinear model训练出来的
        # TODO: 此处使用了article的特征
		article_features_tmp = self.article_features[candidate_article_indexs]

		# TODO:za, 用户与文章的交叉特征
		# za : feature of current user/article combination, k*1
		za = np.outer(article_features_tmp.reshape(-1), self.xa)\
			.reshape((article_len,self.k,1)) # (20,36,1)
		zaT = np.transpose(za, (0,2,1)) # (20,1,36), 将交叉矩阵展开成一维向量

		A0Iza = np.matmul(self.A0I, za) # (20,36,1)
		A0IBaTAaIxa = np.matmul(self.A0IBaTAaI[candidate_article_indexs], self.xa) # (20,36,1)
		AaIxa = self.AaI[candidate_article_indexs].dot(self.xa) # (20,6,1)
		AaIBaA0IBaTAaIxa = np.matmul(self.AaIBa[candidate_article_indexs], A0IBaTAaIxa) # (20,6,1)
		# AaIBaA0IBaTAaIxa = np.matmul(self.AaIBaA0IBaTAaI[candidate_article_indexs], self.xa) # (20,6,1)

		s = np.matmul(zaT, A0Iza - 2*A0IBaTAaIxa) + np.matmul(self.xaT, AaIxa + AaIBaA0IBaTAaIxa) # (20,1,1)
		exploration = self.alpha*np.sqrt(s) # (20,1,1)

		exploitation =  zaT.dot(self.beta) + np.matmul(self.xaT, self.theta[candidate_article_indexs])

		p = exploitation + exploration
		# assert (s < 0).any() == False
		# assert np.isnan(np.sqrt(s)).any() == False

		# print A0Iza.shape, A0IBaTAaIxa.shape, AaIxa.shape, AaIBaA0IBaTAaIxa.shape, s.shape, p.shape (for debugging)
		max_index = np.argmax(p)
		self.z = za[max_index]
		self.zT = zaT[max_index]
		art_max = candidate_article_indexs[max_index]
		self.acticle_max_index = art_max # article candidate_article_indexs with largest UCB

		return candidate_articles[max_index]

