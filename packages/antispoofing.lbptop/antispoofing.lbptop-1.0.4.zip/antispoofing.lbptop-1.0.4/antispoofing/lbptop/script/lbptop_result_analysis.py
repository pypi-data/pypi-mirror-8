#!/usr/bin/env python
#Tiago de Freitas Pereira <tiagofrepereira@gmail.com>
#Fri Jul 27 14:30:00 CEST 2012

"""
This script will run the result analisys for the LBPTOP countermeasure


The procedure is described in the paper: "LBP-TOP based countermeasure against facial spoofing attacks" - de Freitas Pereira, Tiago and Anjos, Andre and De Martino, Jose Mario and Marcel, Sebastien; ACCV - LBP 2012

"""

import os, sys
import argparse
import bob
import numpy

from .. import spoof
from ..spoof import calclbptop

from antispoofing.utils.ml import *
from antispoofing.utils.helpers import *
from antispoofing.utils.db import *

from antispoofing.lbptop.helpers import *

def main():

  ##########
  # General configuration
  ##########

  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)

  parser.add_argument('-s', '--scores-dir', type=str, dest='scoresDir', default='', help='Base directory containing the Scores to a specific protocol  (defaults to "%(default)s")')

  parser.add_argument('-o', '--output-dir', type=str, dest='outputDir', default='', help='Base directory that will be used to save the results.')

  parser.add_argument('-n','--score-normalization',type=str, dest='scoreNormalization',default='', choices=('znorm','minmax',''))

  parser.add_argument('-t', '--thresholds', type=float, dest='thresholds', default=[], help='The predifined thresholds', nargs='+')

  parser.add_argument('-v', '--verbose', action='store_true', dest='verbose', default=False, help='Increases this script verbosity')

  parser.add_argument('-a', '--average-scores', action='store_true', dest='average_scores', default=False, help='Use the average of scores')

  parser.add_argument('-i', '--average-size', type=int, dest='average_size', default=100, help='The number of accumulated frames to compute the average')

  #######
  # Database especific configuration
  #######
  Database.create_parser(parser, implements_any_of='video')

  args = parser.parse_args()

  scoresFolder = ["scores_XY","scores_XT","scores_YT","scores_XT-YT","scores_XY-XT-YT"]
  models = ['XY-plane','XT-Plane','YT-Plane','XT-YT-Plane','XY-XT-YT-plane']
  lines  = ['r','b','y','g^','c']
  energy = 0.0
  scoresRange = (-5,5)

  ## Parsing
  scoresDir          = args.scoresDir
  outputDir          = args.outputDir
  scoreNormalization = args.scoreNormalization
  thresholds         = args.thresholds
  verbose            = args.verbose

  average_scores     = args.average_scores
  average_size       = args.average_size

  predefinedThresholds = False
  if(len(thresholds) > 0):
    predefinedThresholds = True

  if not os.path.exists(scoresDir):
    parser.error("scores-dir directory does not exist")

  if not os.path.exists(outputDir): # if the output directory doesn't exist, create it
    bob.db.utils.makedirs_safe(outputDir)

  #########
  # Loading some dataset
  #########
  if(verbose):
    print("Querying the database ... ")

  database = args.cls(args)

  trainReal, trainAttack = database.get_train_data()
  develReal, develAttack = database.get_devel_data()
  testReal, testAttack   = database.get_test_data()


  #### Storing the scores in order to plot their distribution
  trainRealScores   = []
  trainAttackScores = []

  develRealScores   = []
  develAttackScores = []

  testRealScores    = []
  testAttackScores  = []


  if(not predefinedThresholds):
    thresholds        = []
  
  develTexts        = []
  testTexts        = []

  if(verbose):
    print("Generating test results ....")


  for i in range(len(scoresFolder)):

    scoresPlaneDir = os.path.join(scoresDir,scoresFolder[i])

    #If for some reason the scores directory does not exists, 
    if not os.path.exists(scoresPlaneDir):
      models[i] = models[i] + " scores file not found."

      #Storing the scores
      trainRealScores.append(numpy.zeros(2))
      trainAttackScores.append(numpy.zeros(2))

      develRealScores.append(numpy.zeros(2))
      develAttackScores.append(numpy.zeros(2))

      testRealScores.append(numpy.zeros(2))
      testAttackScores.append(numpy.zeros(2))

      if(not predefinedThresholds):
        thresholds.append(0)
      develTexts.append('')
      testTexts.append('')

      continue

    if(verbose):
      print(models[i])

    #Getting the scores
    realScores   = ScoreReader(trainReal,scoresPlaneDir)
    attackScores = ScoreReader(trainAttack,scoresPlaneDir)
    train_real_scores = realScores.getScores(average=average_scores, average_size=average_size)
    train_attack_scores = attackScores.getScores(average=average_scores, average_size=average_size)

    realScores   = ScoreReader(develReal,scoresPlaneDir)
    attackScores = ScoreReader(develAttack,scoresPlaneDir)
    devel_real_scores = realScores.getScores(average=average_scores, average_size=average_size)
    devel_attack_scores = attackScores.getScores(average=average_scores, average_size=average_size)

    realScores   = ScoreReader(testReal,scoresPlaneDir)
    attackScores = ScoreReader(testAttack,scoresPlaneDir)
    test_real_scores = realScores.getScores(average=average_scores, average_size=average_size)
    test_attack_scores = attackScores.getScores(average=average_scores, average_size=average_size)

    #Applying the score normaliztion
    if(scoreNormalization=="minmax"):
      scoreNorm = ScoreNormalization(numpy.concatenate((train_real_scores,train_attack_scores)))

      train_real_scores   = scoreNorm.calculateMinMaxNorm(train_real_scores)
      train_attack_scores = scoreNorm.calculateMinMaxNorm(train_attack_scores)

      devel_real_scores   = scoreNorm.calculateMinMaxNorm(devel_real_scores)
      devel_attack_scores = scoreNorm.calculateMinMaxNorm(devel_attack_scores)

      test_real_scores   = scoreNorm.calculateMinMaxNorm(test_real_scores)
      test_attack_scores = scoreNorm.calculateMinMaxNorm(test_attack_scores)

      scoresRange = (-1,1)
  
    elif(scoreNormalization=="znorm"):

      train_real_scores   = scoreNorm.calculateZNorm(train_real_scores)
      train_attack_scores = scoreNorm.calculateZNorm(train_attack_scores)

      devel_real_scores   = scoreNorm.calculateZNorm(devel_real_scores)
      devel_attack_scores = scoreNorm.calculateZNorm(devel_attack_scores)

      test_real_scores   = scoreNorm.calculateZNorm(test_real_scores)
      test_attack_scores = scoreNorm.calculateZNorm(test_attack_scores)

 

    if numpy.mean(devel_real_scores) < numpy.mean(devel_attack_scores):
      train_real_scores = train_real_scores * -1; train_attack_scores = train_attack_scores * -1
      devel_real_scores = devel_real_scores * -1; devel_attack_scores = devel_attack_scores * -1
      test_real_scores = test_real_scores * -1; test_attack_scores = test_attack_scores * -1

    
   #### Calculation of the error rates for one plane
    if(predefinedThresholds):
      (test_hter,devel_hter),(test_text,devel_text) = perf.perf_hter_threshold([test_real_scores,test_attack_scores], [devel_real_scores,devel_attack_scores], thresholds[i])
    else:
      (test_hter,devel_hter),(test_text,devel_text),thres = perf.perf_hter([test_real_scores,test_attack_scores], [devel_real_scores,devel_attack_scores], bob.measure.eer_threshold)
       

    #Storing the scores
    trainRealScores.append(train_real_scores)
    trainAttackScores.append(train_attack_scores)

    develRealScores.append(devel_real_scores)
    develAttackScores.append(devel_attack_scores)

    testRealScores.append(test_real_scores)
    testAttackScores.append(test_attack_scores)

    #Storing the protocol issues for each plane
    if(not predefinedThresholds):
      thresholds.append(thres)
    develTexts.append(devel_text)
    testTexts.append(test_text)


  perf_lbptop.saveCounterMeasureResults(trainRealScores,trainAttackScores,develRealScores,develAttackScores,testRealScores,testAttackScores,thresholds,models,lines,develTexts,testTexts,energy,outputDir,scoresRange=scoresRange)
 
  return 0


if __name__ == "__main__":
  main()
