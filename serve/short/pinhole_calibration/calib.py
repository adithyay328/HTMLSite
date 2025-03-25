"""
Let's implement pinhole calibration on some images
with some GT intrisics. Should make it easy
to check for mistakes.
"""
import os
import random
from copy import deepcopy

import numpy as np
import cv2
import matplotlib.pyplot as plt
import PIL.Image as Image

# Spotify's nearest neighbour library.
# FAISS is good and I like it but
# hard to pip install, and annoy,
# Spotify's last one, is deprecated
# in favor of Voyager.
from voyager import Index, Space

# Hardcoded k-matrix from calibration
# off my iphone; this is our expected
# GT.
K = np.array([
  [ 1412.1646, 0, 959.8695],
  [ 0, 1416.3217, 543.6796],
  [ 0, 0, 1]
])

def drawPts ( mat, pts, radius=10):
  for pt in pts:
    cv2.circle(mat, (int(pt.pt[0]), int(pt.pt[1])), radius, (0, 255, 0), 2)

  plt.imshow(mat)
  plt.show()

def getAllFeaturePoints(mat):
  """
  Given a mat, just find me
  every possible point
  you can. This should contain
  all of the calibration points,
  and more
  """

  # Run ORB, find me all
  # points 
  orb = cv2.ORB_create(1000)
  pts, des = orb.detectAndCompute(mat, None)

  # drawPts(mat, pts)

  return list ( pts )

def nonMaxSupress(mat, pts, radius = 30):
  """
  Given a bunch of points in a matrix,
  as well as a minimum radius, takes
  clusters of points and replaces all
  their pts with one at the mean
  """
  i = 0
  while i < len ( pts ):
    # Compute all pts within
    # the radius. Just use
    # brute force here
    matchingIndices = [i]

    for j in range(i + 1, len(pts)):
      if np.linalg.norm ( np.array(pts[i].pt) - np.array(pts[j].pt) ) <= radius:
        matchingIndices.append(j)

    # Take mean of all those points
    allPoints = np.array([ pts[j].pt for j in matchingIndices ])
    mean = np.mean(allPoints, axis=0)

    # Replace current point center with that
    pts[i].pt = tuple ( mean.reshape(-1).tolist() )

    # Delete those other indices
    for idx in reversed(matchingIndices[1:]):
      del pts[idx]
  
    i += 1

  return pts

def bwOnly ( mat, pts, region : float = 0.02, dist = 0.37, samples : int = 10):
  """
  A really simple filter that works on black and white only.

  Run through all keypoints, and remove those where in a small
  neighbourhood around the corner, I can't see a strong black
  and strong white.
  """
  idxToRemove = []

  print ( mat.shape )
  MAX_X_DISTANCE = int(region * mat.shape[1])
  MAX_Y_DISTANCE = int(region * mat.shape[0])

  for pt in pts:
    center = np.array(pt.pt).astype(int)

    foundBlack = False
    foundWhite = False
    
    for sample in range ( samples ):
      if foundBlack and foundWhite:
        break

      randOffset = np.random.randn ( 2 ) * np.array([MAX_X_DISTANCE, MAX_Y_DISTANCE])
      sample = ( center + randOffset ).astype(int)

      sample[0] = min ( max ( 0, sample[0] ), mat.shape[1] - 1 )
      sample[1] = min ( max ( 0, sample[1] ), mat.shape[0] - 1 )

      print ( sample )
      color = mat[sample[1], sample[0]].astype(float) / 255

      print ( color )

      if np.linalg.norm(color - np.array([0, 0, 0])) < dist:
        foundBlack = True
      elif np.linalg.norm(color - np.array([1, 1, 1])) < dist:
        foundWhite = True

    if not ( foundBlack and foundWhite ):
      idxToRemove.append(pt)

  for idx in reversed(idxToRemove):
    pts.remove(idx)

  return pts

def scorePts ( mat, allPoints ):
  # Make mat b + w
  mat = cv2.cvtColor(mat, cv2.COLOR_BGR2GRAY)

  RADIUS = 10
  # Convert all points to np arrays of [ x, y ]

  nps = [ np.array ( pt.pt ) for pt in allPoints ]

  initScores = [ ]

  for idx in range ( len ( nps ) ):
    # Run 30 times per point, and take the
    # top 5 biggest gradient deltas
    currScores = []

    for iters in range ( 30 ):
      # In each iteration, compare out index to
      # some pixel near us
      rand = np.random.randn(2) * RADIUS

      idx1 = ( nps [ idx ] ).astype(int)
      idx2 = ( nps [ idx ] + rand.clip ( 0, mat.shape[0] - 1 ) ).astype(int)

      intensity1 = int ( mat [ idx1[1], idx1[0] ] )
      intensity2 = int ( mat [ idx2[1], idx2[0] ] )

      diff = abs ( intensity1 - intensity2 )
      print ( diff )

      currScores.append( diff ** 3 )

    TOP_K = 7
    score = sum ( sorted ( currScores, reverse=True )[:TOP_K] )

    initScores.append ( score )

  # Now, one more step; for each
  # point, add the scores of its 2 nearest neighbours
  index = Index(Space.Euclidean, num_dimensions=2)
  for pt in allPoints:
    index.add_item ( np.array ( pt.pt ) )
  
  finalScore = []

  for sourceIdx in range ( len ( nps ) ):
    nearestNeighbourIdxs, _ = index.query ( nps [ sourceIdx ], k=4 )
    # Ignore ourselves
    nearestNeighbourIdxs = nearestNeighbourIdxs[1:]

    currScore = initScores [ sourceIdx ]

    currScore += sum ( [ initScores [ idx ] for idx in nearestNeighbourIdxs ] )

    finalScore.append ( currScore )

  return zip ( allPoints, finalScore )

# def findIndicesWithin(pointOne: np.ndarray, pointTwo: np.ndarray, allPoints: np.ndarray, maxDist : float):
#   """
#   Given 2 points that define a line, finds the
#   indices of all points within a certain
#   euclidean distance to the line.
#   """
#   # First get the whole thing as a vector that
#   # goes through the origin
#   directionVector = pointTwo - pointOne
#   # Solve for when x = 0 i.e. y offset
#   yOffset = pointOne[1] - directionVector[1] * ( pointOne[0] / directionVector[0] )
# 
#   # Subtract that from all point ys.
#   allPoints[:, 1] -= yOffset
# 
#   # Project onto direction vector and find the distance
#   unitDir = directionVector / np.linalg.norm(directionVector)
#   projs = np.dot(allPoints, unitDir).reshape(-1, 1) * unitDir
#   resid = allPoints - projs
#   dists = np.linalg.norm(resid, axis=1)
# 
#   # Just return argwhere
#   return np.argwhere(dists < maxDist).reshape ( -1 )

# def findRectangleCorners ( img, pts, MAX_ITERS = 10000 ):
#   """
#   Given a set of NMSsed points,
#   returns those which are part of a
#   rectangle, not-necessairly in any
#   order.
# 
#   I haven't looked up how people normally do this,
#   but RANSAC to try and find the other corners has
#   got to be one of the ways.
#   """
#   imgX = img.shape[1]
#   imgY = img.shape[0]
# 
#   originalPts = deepcopy([ pt.pt for pt in pts ])
#   
#   # Make an L2 index
#   # of all the points. Much
#   # faster than brute-force
#   # searching
#   index = Index(Space.Euclidean, num_dimensions=2)
# 
#   for pt in pts:
#     asList = list ( pt.pt )
#     index.add_item ( asList )
# 
#   for it in range ( MAX_ITERS ):
#     # Pick 1 random start index
#     firstIndex = random.randint(0, len(pts) - 1)
# 
#     # Pick 2 nearest neighbours as the neighbours
#     neighbors, distances = index.query ( list ( pts[firstIndex].pt ), k=3 )
# 
#     # Ignore first neighbour since it should be this point
#     neighbors, distances = neighbors[1:], distances[1:]
# 
#     # Find both direction vectors
#     # from the first point to others
#     disp1 = np.array(pts[firstIndex].pt) - np.array(pts[neighbors[0]].pt)
#     disp2 = np.array(pts[firstIndex].pt) - np.array(pts[neighbors[1]].pt)
# 
#     # Now, find all indices that are co-linear with either of those
#     # points. Since we're using normalized coordinates
#     # now, just use any that are within 2% of expected image
#     # coordinates
# 
#     # To compute the bound, construct a vector that is 1%
#     # of the x, 2% of the y, and take its norm
#     normToUse = np.linalg.norm ( np.array([0.01 * imgX, 0.01 * imgY]) )
# 
#     disp1Matches = findIndicesWithin(np.array(pts[firstIndex].pt), np.array(pts[neighbors[0]].pt), np.array([pt.pt for pt in pts]), normToUse)
#     disp2Matches = findIndicesWithin(np.array(pts[firstIndex].pt), np.array(pts[neighbors[1]].pt), np.array([pt.pt for pt in pts]), normToUse)
# 
#     # Now, plot all the points found. use blue for found all found points,
#     # green for the neighbours, and red for the source
#     disp1MatchedPoints = [ pts[i].pt for i in disp1Matches ]
#     disp2MatchedPoints = [ pts[i].pt for i in disp2Matches ]
#     plt.imshow(img)
#     plt.scatter([disp1MatchedPoints[i][0] for i in range(len(disp1MatchedPoints))], [disp1MatchedPoints[i][1] for i in range(len(disp1MatchedPoints))], c='blue')
#     plt.scatter([disp2MatchedPoints[i][0] for i in range(len(disp2MatchedPoints))], [disp2MatchedPoints[i][1] for i in range(len(disp2MatchedPoints))], c='blue')
#     plt.scatter([pts[firstIndex].pt[0]], [pts[firstIndex].pt[1]], c='red')
#     plt.scatter([pts[neighbors[0]].pt[0]], [pts[neighbors[0]].pt[1]], c='green')
#     plt.scatter([pts[neighbors[1]].pt[0]], [pts[neighbors[1]].pt[1]], c='green')
#     plt.show()

if __name__ == "__main__":
  # All images are titled *.jpeg
  imageNames = [ f for f in os.listdir(".") if "jpeg" in f ]

  images = [ Image.open ( name ) for name in imageNames ]

  # Reshape all images to 1920 x 1080
  # to match what the camera calib
  # above was done with
  images = [ img.resize( (1920, 1080) ) for img in images ]

  # For now just focus on image 1
  img = np.array( images[0] )

  features = getAllFeaturePoints(img)
  features = nonMaxSupress(img, features)
  # features = bwOnly(img, features)

  featuresScores = sorted ( scorePts(img, features), key = lambda x: x[1], reverse=True)

  allScores = [ x[1] for x in featuresScores ]

  plt.hist(allScores, bins=100)
  plt.show()

  # We have 80 pts, keep those
  NUM_CORNERS = 80

  features = [ x[0] for x in featuresScores[:NUM_CORNERS] ]

  drawPts(img, features)


  exit(0)

  # findRectangleCorners(img, features)
