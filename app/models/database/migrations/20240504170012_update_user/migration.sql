/*
  Warnings:

  - You are about to drop the column `pictrue` on the `Assets` table. All the data in the column will be lost.
  - Added the required column `picture` to the `Assets` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Assets" DROP COLUMN "pictrue",
ADD COLUMN     "picture" JSONB NOT NULL;
